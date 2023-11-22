import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, normalize_whitespace, unformat_date

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
    skipped_count = 0
    today = today_date_string()
    for div in event_title_elements:
        time_place_location_values = div.find_next_sibling("p").find_all("span", class_="value")
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""
        if len(time_place_location_values) > 0:
            start = time_place_location_values[0].text.strip()
            if start.endswith(" Uhr"):
                start = start[:-4]
        if len(time_place_location_values) > 1:
            end = time_place_location_values[1].text.strip()
            if end.endswith(" Uhr"):
                end = end[:-4]
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        location = ""
        if len(time_place_location_values) > 2:
            location = time_place_location_values[2].text.strip()
        title = div.find("a").text.strip()
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
    return events, f"({skipped_count} skipped)"
