import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, normalize_whitespace, get_date_matches, get_time_matches, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("article")
    description = ""
    start = ""
    end = ""
    location = ""
    if content_div:
        time_element = content_div.find("time")
        if time_element:
            date_matches = get_date_matches(time_element.get_text())
            time_matches = get_time_matches(time_element.get_text())
            if len(date_matches) > 0 and len(time_matches) > 0:
                start = f"{date_matches[0]} {time_matches[0]}"
            if len(date_matches) > 1 and len(time_matches) > 1:
                end = f"{date_matches[1]} {time_matches[1]}"
        location_element = content_div.find("div", class_="field--name-field-location")
        if location_element:
            location = location_element.get_text(strip=True)
        description_element = content_div.find("div", class_="field--name-field-body")
        if description_element:
            description = normalize_whitespace(description_element.get_text())
    return description, start, end, location

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("main").find_all("tr")
    events = []
    skipped_count = 0
    today = today_date_string()
    for event_element in event_elements:
        # Skip the first row, which is the table header
        if event_element.find("th"):
            continue
        event_row_columns = event_element.find_all("td")
        date_column = event_row_columns[0]
        title_column = event_row_columns[1]
        
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""
        date_matches = get_date_matches(date_column.get_text(strip=True))
        if len(date_matches) > 1:
            start = date_matches[0]
            end = date_matches[1]

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        title = ""
        title_element = title_column.find("a")
        if title_element:
            title = title_element.get_text(strip=True)
            link = "https://www.arl-net.de" + title_element["href"]
        
        description = ""
        location = ""
        if options.get("parse_details_pages", True):
            description, start_details, end_details, location = parse_details_page(link)
            if start_details != "":
                start = start_details
            if end_details != "":
                end = end_details

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
