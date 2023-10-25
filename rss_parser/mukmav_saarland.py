from datetime import date
from rss_parser import generic_rss_parser
from event import Event

def parse(feed_url):
    parsed_data = generic_rss_parser.fetch_and_parse_feed(feed_url)
    events = []
    today = date.today().strftime("%d.%m.%Y")
    for entry in parsed_data:
        event = Event(
            title=entry.title,
            link=entry.link,
            added=today,
        )
        events.append(event)
    return events