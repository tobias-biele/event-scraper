# TODO: Extract date, time, topic and target group from description

from event import Event
from .difu_html import parse_details_page
from .utils import fetch_and_parse_rss_feed, today_date_string, unformat_date

def parse(feed_url, options):
    parsed_data = fetch_and_parse_rss_feed(feed_url)
    events = []
    today = today_date_string()
    for entry in parsed_data:
        start = ""
        end = ""
        timeframe = ""
        location = ""
        if options["parse_details_pages"]:
            details = parse_details_page(entry.link)
            if details["start"]:
                start = details["start"]
            if details["end"]:
                end = details["end"]
            if details["timeframe"]:
                timeframe = details["timeframe"]
            if details["location"]:
                location = details["location"]

        # Skip the event if it's before the cut-off date
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            continue

        event = Event(
            title=entry.title,
            actor="Deutsches Institut für Urbanistik",
            start=start,
            end=end,
            timeframe=timeframe,
            location=location,
            link=entry.link,
            added=today,
            description=entry.description,
        )
        events.append(event)
    return events