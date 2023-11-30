import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, normalize_whitespace, get_date_matches, get_time_matches, unformat_date

def parse_details_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    } # BUND blocks standard requests from the requests library, therefore we need to set a user agent
    details_page = requests.get(url, headers=headers)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", id="anchor-description")
    description = ""
    timeframe = ""
    actor = ""
    if content_div:
        description = normalize_whitespace(content_div.get_text())
    participate_text_element = details_soup.find("b", string="HOW TO PARTICIPATE")
    if participate_text_element:
        participate_text = participate_text_element.parent.get_text()
        split_lines = participate_text.split("\n")
        if len(split_lines) > 1:
            second_line = participate_text.split("\n")[1]
            if " | " in second_line:
                timeframe = second_line.split(" | ")[1]
            elif ", " in second_line:
                timeframe = second_line.split(", ")[1]
    return description, timeframe

def parse(url, options):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    } # BUND blocks standard requests from the requests library, therefore we need to set a user agent
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="cmcc-masonry").find_all("div", class_="cmcc-vc-events")
    events = []
    skipped_count = 0
    today = today_date_string()
    for event_element in event_elements:
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""

        dates_div = event_element.find("div", class_="dates")
        if dates_div:
            day = dates_div.find("span", class_="day").get_text(strip=True)
            month = dates_div.find("span", class_="month").get_text(strip=True)
            year = dates_div.find("span", class_="year").get_text(strip=True)
            start = format_date(f"{day} {month} {year}")

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        title = ""
        link = ""
        title_element = event_element.find("div", class_="cmcc-event-title").find("a")
        if title_element:
            title = title_element.get_text(strip=True)
            link = title_element["href"]
        location = ""
        location_element = event_element.find("div", class_="location")
        if location_element:
            location = location_element.get_text(strip=True)
        
        timeframe = ""
        description = ""
        if options.get("parse_details_pages", True):
            description, timeframe = parse_details_page(link)

        event = Event(
            title=title,
            start=start,
            end=end,
            timeframe=timeframe,
            location=location,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events, f"({skipped_count} skipped)"
