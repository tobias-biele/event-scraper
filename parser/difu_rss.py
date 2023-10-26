# TODO: Extract date, time, topic and target group from description

from event import Event
from .difu_html import parse_details_page
from .utils import fetch_and_parse_rss_feed, today_date

def parse(feed_url, options):
    parsed_data = fetch_and_parse_rss_feed(feed_url)
    events = []
    today = today_date()
    for entry in parsed_data:
        start = ""
        end = ""
        timeframe = ""
        if options["parse_details_pages"]:
            details = parse_details_page(entry.link)
            if details["start"]:
                start = details["start"]
            if details["end"]:
                end = details["end"]
            if details["timeframe"]:
                timeframe = details["timeframe"]

        event = Event(
            title=entry.title,
            actor="Deutsches Institut für Urbanistik",
            start=start,
            end=end,
            timeframe=timeframe,
            link=entry.link,
            added=today,
        )
        events.append(event)
    return events