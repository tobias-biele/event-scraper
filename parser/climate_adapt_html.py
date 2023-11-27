import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, unformat_date

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="event_listing").find_all("article")
    events = []
    skipped_count = 0
    today = today_date_string()
    for element in event_elements:
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""
        timeframe = ""

        start_element = element.find("span", class_="datedisplay")
        if start_element:
            start = start_element.get_text()
            starttime = element.find("abbr", class_="dtstart")
            endtime = element.find("abbr", class_="dtend")
            timeframe = f"von {starttime.get_text()} bis {endtime.get_text()}"
        else:
            start_element = element.find("abbr", class_="dtstart")
            end_element = element.find("abbr", class_="dtend")
            if start_element:
                start = start_element.get_text(strip=True)
            if end_element:
                end = end_element.get_text(strip=True)

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        title = element.find("h2").get_text(strip=True)
        link = element.find("h2").find("a")["href"]
        location = ""
        location_element = element.find("div", class_="location")
        if location_element:
            location = location_element.get_text(strip=True)

        description = ""
        description_element = element.find("p", class_="description")
        if description_element:
            description = description_element.get_text(strip=True)

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
