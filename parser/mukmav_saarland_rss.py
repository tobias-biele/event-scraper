from datetime import date
from event import Event
from .utils import fetch_and_parse_rss_feed, today_date

def parse(feed_url):
    parsed_data = fetch_and_parse_rss_feed(feed_url)
    events = []
    today = today_date()
    for entry in parsed_data:
        event = Event(
            title=entry.title,
            link=entry.link,
            added=today,
        )
        events.append(event)
    return events