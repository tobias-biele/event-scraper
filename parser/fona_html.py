import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, get_date_matches, normalize_whitespace, unformat_date

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
    skipped_count = 0
    today = today_date_string()
    for element in event_element:
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""
        date_div = element.find("span", class_="item--date")
        if date_div:
            date_matches = get_date_matches(date_div.text.strip())
            if len(date_matches) > 0:
                start = date_matches[0]
            if len(date_matches) > 1:
                end = date_matches[1]
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue
        
        content_div = element.find("div", class_="item--content")
        title = content_div.find("a").find("span").text.strip()
        link = "https://www.fona.de" + content_div.find("a")["href"]

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
    return events, f"({skipped_count} skipped)"
