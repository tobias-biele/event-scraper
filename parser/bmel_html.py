import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date, normalize_whitespace

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="content")
    description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_title_elements = soup.find_all("h2", class_="c-searchteaser__h")
    events = []
    today = today_date()
    for div in event_title_elements:
        time_place_location_values = div.find_next_sibling("p").find_all("span", class_="value")
        title = div.find("a").text.strip()
        start = ""
        end = ""
        location = ""
        if len(time_place_location_values) > 0:
            start = time_place_location_values[0].text.strip()
        if len(time_place_location_values) > 1:
            end = time_place_location_values[1].text.strip()
        if len(time_place_location_values) > 2:
            location = time_place_location_values[2].text.strip()
        link = "https://www.bmel.de/" + div.find("a")["href"]

        description = ""
        if options.get("parse_details_pages", True):
            description = parse_details_page(link)
        
        event = Event(
            title=title,
            start=start,
            end=end,
            actor="Bundesministerium für Ernährung und Landwirtschaft",
            location=location,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events
