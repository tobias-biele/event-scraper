import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, unformat_date

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")

    event_section = soup.find("div", class_="et_pb_tab_content")
    events = []
    today = today_date_string()
    i = 0
    start = ""
    title = ""
    skip_event = False
    for event_text in event_section.stripped_strings:
        event_text = event_text.replace('\xad', '')
        if i == 0 or i == 2 and len(event_text) < 20: # if the text is a date, it will be shorter than 20 characters
            start = format_date(event_text, 1)
            if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
                skip_event = True # skip the event if it's before the cut-off date
            i += 1
        elif i == 1:
            title = event_text
            if not skip_event:
                event = Event(
                    title=title,
                    start=start,
                    added=today,
                )
                events.append(event)
            start = ""
            title = ""
            skip_event = False
            i = 0
    return events
