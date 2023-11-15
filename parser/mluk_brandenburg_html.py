import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, get_date_matches, get_time_matches, unformat_date

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("table").find_all("tr")
    events = []
    today = today_date_string()
    for element in event_elements:
        columns = element.find_all("td")
        date_text = columns[0].get_text(strip=True)
        date_matches = get_date_matches(date_text)
        time_matches = get_time_matches(date_text)
        start = ""
        timeframe = ""
        if len(date_matches) > 0:
            start = date_matches[0]
        if len(time_matches) > 0:
            timeframe = time_matches[0]

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            continue

        event_text_column = columns[1]
        title = event_text_column.find("strong").get_text(strip=True)
        location = ""
        description = event_text_column.get_text().split("Ort:")[0].strip()
        location = event_text_column.get_text().split("Ort:")[1].strip()

        event = Event(
            title=title,
            start=start,
            timeframe=timeframe,
            location=location,
            added=today,
            description=description,
        )
        events.append(event)
    return events
