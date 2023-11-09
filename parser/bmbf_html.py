import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date, get_date_matches, normalize_whitespace

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    description = normalize_whitespace(details_soup.get_text())
    return description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_divs = soup.find_all("a", class_="c-teaser")
    events = []
    today = today_date()
    for div in event_divs:
        event_title_element = div.find("h2", class_="c-teaser__headline")
        title = event_title_element.find("span").text.strip()
        link = div["href"]
        date_divs = div.find_all("time")
        start = ""
        end = ""
        if len(date_divs) > 0:
            start = date_divs[0].text.strip()
        if len(date_divs) > 1:
            end = get_date_matches(date_divs[1].text.strip())[0]
        location = ""
        location_div = div.find("span", class_="c-topline__location")
        if location_div:
            location = location_div.text.strip()
            if "Ort: " in location:
                location = location.split("Ort: ")[1].strip()

        description = ""
        if options.get("parse_details_pages", True):
            description = parse_details_page(link)
        
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
