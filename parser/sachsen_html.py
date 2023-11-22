import locale
import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, unformat_date

locale.setlocale(locale.LC_TIME, "de_DE")

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="panel-group").find_all("div", class_="panel panel-default")
    events = []
    skipped_count = 0
    today = today_date_string()
    for element in event_elements:
        heading_element = element.find("div", class_="panel-heading")
        start = ""
        location = ""
        if heading_element:
            heading = heading_element.find("a").text
            location = heading.split(" am")[0]
            # Get the start date of the event and skip it if it's before the cut-off date
            date_string = heading.split("am ")[1]
            start = format_date(date_string, format_type=1)
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        collapse_element = element.find("div", class_="panel-collapse")
        title = collapse_element.find("h4").get_text()
        link = "https://www.klima.sachsen.de" + collapse_element.find("ul", class_="list-links").find("a").get("href")
        
        # For more details, the linked PDF would have to be parsed

        event = Event(
            title=title,
            start=start,
            location=location,
            link=link,
            added=today,
        )
        events.append(event)
    return events, f"({skipped_count} skipped)"
