# TODO: Needs to be reworked since the website has changed

import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="s-richtext")
    description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    coming_events_headline = soup.select_one('h2:-soup-contains("Anstehende Veranstaltungen")')
    if coming_events_headline == None:
        return [], ""
    event_section = coming_events_headline.find_next_sibling("section")
    a_tags = event_section.find_all("a")
    events = []
    skipped_count = 0
    today = today_date_string()
    start = ""
    title = ""
    i = 0
    skip_event = False
    for event_text in event_section.stripped_strings:
        if i == 0 or i == 2 and len(event_text) < 20: # if the text is a date, it will be shorter than 20 characters
            start = event_text
            if start[-1] == ":":
                start = start[:-1]
            start = format_date(start, 1)
            if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
                skipped_count += 1
                skip_event = True # skip the event if it's before the cut-off date
            i += 1
        elif i == 1:
            title = event_text
            if title.startswith(": "):
                title = title[2:]
            if title.endswith(","):
                title = title[:-1]
            i += 1
        else:
            if len(event_text) >= 20 and len(a_tags) > 0: # if the text is a link to "weitere Informationen", it will be at least 20 characters long
                link = a_tags.pop(0).get("href")
            if not skip_event:
                event = Event(
                    title=title,
                    start=start,
                    link=link,
                    added=today,
                )
                events.append(event)
            skip_event = False
            start = ""
            title = ""
            link = ""
            i = 0
    if i == 2: # if the last event has no link, we still have to add it
        if not skip_event:
            event = Event(
                title=title,
                start=start,
                link=link,
                added=today,
            )
            events.append(event)
    return events, f"({skipped_count} skipped)"
