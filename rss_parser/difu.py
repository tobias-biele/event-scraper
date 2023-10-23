# TODO: Extract date, time, topic and target group from description

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
            actor="Deutsches Institut für Urbanistik",
            link=entry.link,
            added=today,
        )
        events.append(event)
    return events