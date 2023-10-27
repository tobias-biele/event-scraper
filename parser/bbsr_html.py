import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date, format_date

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_title_elements = soup.find_all("h4")
    events = []
    today = today_date()
    for div in event_title_elements:
        title = div.find("a").find("span").text.strip()
        link = "https://www.bbsr.bund.de/" + div.find("a")["href"].split(";")[0]
        time_divs = div.find_all("time")
        if len(time_divs) > 0:
            start = format_date(time_divs[0]["datetime"])
        if len(time_divs) > 1:
            end = format_date(time_divs[1]["datetime"])

        event = Event(
            title=title,
            start=start,
            end=end,
            link=link,
            added=today,
        )
        events.append(event)
    return events
