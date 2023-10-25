# TODO: Extract date, time, topic and target group from description

from event import Event
from .bmuv_html import parse_details_page
from .utils import fetch_and_parse_rss_feed, today_date

def parse(feed_url):
    parsed_data = fetch_and_parse_rss_feed(feed_url)
    events = []
    today = today_date()
    for entry in parsed_data:
        # Parse details page to get start and end time
        start = ""
        try:
            print(f"Parsing details page for {entry.link}")
            details = parse_details_page(entry.link)
            if details["date"]:
                start = details["date"]
            if details["timeframe"]:
                timeframe = details["timeframe"]
        except Exception as e:
            print(f"Error parsing details page for {entry.link}: {e}")

        event = Event(
            title=entry.title,
            actor="Bundesministerium für Umwelt, Naturschutz und nukleare Sicherheit",
            start=start,
            timeframe=timeframe,
            link=entry.link,
            added=today,
        )
        events.append(event)
    return events