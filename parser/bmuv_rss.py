# TODO: Extract topic and target group from description

from event import Event
from .bmuv_html import parse_details_page
from .utils import fetch_and_parse_rss_feed, today_date

def parse(feed_url, options):
    parsed_data = fetch_and_parse_rss_feed(feed_url)
    events = []
    today = today_date()
    for entry in parsed_data:
        start = ""
        timeframe = ""
        if options["parse_details_pages"]:
            # Parse event details page to get date and timeframe
            try:
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