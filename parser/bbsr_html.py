import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, unformat_date, normalize_whitespace

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="s-richtext")
    description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_title_elements = soup.find_all("h4")
    events = []
    skipped_count = 0
    today = today_date_string()
    for div in event_title_elements:
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""
        time_divs = div.find_all("time")
        if len(time_divs) > 0:
            start = format_date(time_divs[0]["datetime"])
        if len(time_divs) > 1:
            end = format_date(time_divs[1]["datetime"])
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue
        
        title = div.find("a").find("span").text.strip()
        link = "https://www.bbsr.bund.de/" + div.find("a")["href"].split(";")[0]

        description = ""
        if options.get("parse_details_pages", True):
            description = parse_details_page(link)

        event = Event(
            title=title,
            start=start,
            end=end,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events, f"({skipped_count} skipped)"
