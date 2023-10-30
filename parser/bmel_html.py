import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date, format_date

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_title_elements = soup.find_all("h2", class_="c-searchteaser__h")
    events = []
    today = today_date()
    for div in event_title_elements:
        time_and_place_values = div.find_next_sibling("p").find_all("span", class_="value")
        title = div.find("a").text.strip()
        start = ""
        end = ""
        if len(time_and_place_values) > 0:
            start = time_and_place_values[0].text.strip()
        if len(time_and_place_values) > 1:
            end = time_and_place_values[1].text.strip()
        link = "https://www.bmel.de/" + div.find("a")["href"]
        event = Event(
            title=title,
            start=start,
            end=end,
            actor="Bundesministerium für Ernährung und Landwirtschaft",
            link=link,
            added=today,
        )
        events.append(event)
    return events
