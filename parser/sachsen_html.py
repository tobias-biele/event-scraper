import locale
import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date

locale.setlocale(locale.LC_TIME, "de_DE")

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="panel-group").find_all("div", class_="panel panel-default")
    events = []
    today = today_date_string()
    for element in event_elements:
        heading_element = element.find("div", class_="panel-heading")
        collapse_element = element.find("div", class_="panel-collapse")
        title = collapse_element.find("h4").get_text()
        link = "https://www.klima.sachsen.de" + collapse_element.find("ul", class_="list-links").find("a").get("href")
        location = ""
        start = ""
        if heading_element:
            heading = heading_element.find("a").text
            location = heading.split(" am")[0]
            date_string = heading.split("am ")[1]
            start = format_date(date_string, format_type=1)

        # For more details, the linked PDF would have to be parsed

        event = Event(
            title=title,
            start=start,
            location=location,
            link=link,
            added=today,
        )
        events.append(event)
    return events
