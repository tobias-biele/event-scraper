from datetime import datetime
from rss_parser import generic_rss_parser
from event import Event

def parse(feed_url):
    parsed_data = generic_rss_parser.fetch_and_parse_feed(feed_url)
    events = []
    current_time = datetime.now()
    for entry in parsed_data:
        event = Event(
            title=entry.title,
            actor="Bundesministerium für Umwelt, Naturschutz und nukleare Sicherheit",
            link=entry.link,
            added=current_time,
        )
        events.append(event)
    return events