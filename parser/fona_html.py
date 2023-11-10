import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, get_date_matches, normalize_whitespace

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("article", class_="sp-default")
    description = normalize_whitespace(content_div.get_text())
    location = ""
    location_element = content_div.find("span", class_="content--location")
    if location_element:
        location = location_element.text.strip()
    return description, location

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_element = soup.find("div", class_="teaser--list").find_all("article")
    events = []
    today = today_date_string()
    for element in event_element:
        content_div = element.find("div", class_="item--content")
        title = content_div.find("a").find("span").text.strip()
        link = "https://www.fona.de" + content_div.find("a")["href"]
        start = ""
        end = ""
        date_div = element.find("span", class_="item--date")
        if date_div:
            date_matches = get_date_matches(date_div.text.strip())
            if len(date_matches) > 0:
                start = date_matches[0]
            if len(date_matches) > 1:
                end = date_matches[1]

        description = content_div.find("p").text.strip()
        location = ""
        if options.get("parse_details_pages", True):
            description, location = parse_details_page(link)
        
        event = Event(
            title=title,
            start=start,
            end=end,
            location=location,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events
