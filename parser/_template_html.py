import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, normalize_whitespace, get_date_matches, get_time_matches, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="...")
    description = ""
    if content_div:
        description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="results-events").find_all("article")
    events = []
    skipped_count = 0
    today = today_date_string()
    for event_element in event_elements:
        print(event_element.prettify())
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        title = ""
        # title_element = event_element.find("...", class_="...")
        # if title_element:
        #     title = title_element.get_text(strip=True)
        link = ""
        location = ""
        timeframe = ""

        description = ""
        if options.get("parse_details_pages", True):
            description = parse_details_page(link)

        event = Event(
            title=title,
            start=start,
            end=end,
            timeframe=timeframe,
            location=location,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events, f"({skipped_count} skipped)"

# Remove these three lines after testing the parser
# You can execute this parser module individually by running `<Path to project directory>/venv/bin/python -m parser.<parser_module_name>`
print(parse("Add URL here", {"parse_details_pages": False}))