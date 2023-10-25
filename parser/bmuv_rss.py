# TODO: Extract date, time, topic and target group from description

from event import Event
from .utils import fetch_and_parse_rss_feed, today_date

def parse(feed_url):
    parsed_data = fetch_and_parse_rss_feed(feed_url)
    events = []
    today = today_date()
    for entry in parsed_data:
        event = Event(
            title=entry.title,
            actor="Bundesministerium für Umwelt, Naturschutz und nukleare Sicherheit",
            link=entry.link,
            added=today,
        )
        events.append(event)
    return events