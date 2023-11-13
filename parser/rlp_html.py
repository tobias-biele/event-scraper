# TODO: Probably needs to be adapted next year (2024)

import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, normalize_whitespace, get_date_matches, get_time_matches

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    content_element = soup.find("div", id="content")
    title = normalize_whitespace(content_element.find("h1").get_text())
    description = ""
    description_element = content_element.find("div", class_="ce-bodytext")
    if description_element:
        description = normalize_whitespace(description_element.get_text())
    link = description_element.find("a")["href"]
    date_matches = get_date_matches(description)
    time_matches = get_time_matches(description)
    start = date_matches[0] if len(date_matches) > 0 else ""
    end = date_matches[1] if len(date_matches) > 1 else ""
    timeframe = ""
    if len(time_matches) > 1:
        timeframe = time_matches[0] if len(time_matches) == 1 else f"{time_matches[0]} - {time_matches[1]}"
    
    events = []
    today = today_date_string()
    event = Event(
        title=title,
        start=start,
        end=end,
        timeframe=timeframe,
        link=link,
        added=today,
        description=description,
    )
    events.append(event)
    return events
