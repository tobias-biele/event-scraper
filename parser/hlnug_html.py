import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, normalize_whitespace, get_date_matches, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="ce-bodytext")
    description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="main").find_all("div", class_="frame")
    events = []
    today = today_date_string()
    for element in event_elements[1:]: # skip main headline element
        body_element = element.find("div", class_="ce-bodytext")
        title = element.find("h2").get_text(strip=True)
        description = body_element.find("p").get_text()
        date_patterns = [
            r'(\d{2}.\d{2}.\d{4})', 
            r'(\d{2}.\d{2}.\d{2})', 
            r'\b\d{1,2}\.\s(?:Jan(?:uar)?|Feb(?:ruar)?|März|Apr(?:il)?|Mai|Jun(?:i)?|Jul(?:i)?|Aug(?:ust)?|Sep(?:tember)?|Okt(?:ober)?|Nov(?:ember)?|Dez(?:ember)?)\b \d{4}',
            r'\b\d{1,2}\.\s(?:Jan(?:uar)?|Feb(?:ruar)?|März|Apr(?:il)?|Mai|Jun(?:i)?|Jul(?:i)?|Aug(?:ust)?|Sep(?:tember)?|Okt(?:ober)?|Nov(?:ember)?|Dez(?:ember)?)\b'
        ]
        # Get the dates of the event and stop it if it's before the cut-off date
        # In the case of HLNUG we do not skip the event, but stop parsing the page because the events are ordered chronologically and for many events the date cannot be parsed
        start = ""
        for i, pattern in enumerate(date_patterns):
            date_matches_title = get_date_matches(title, pattern=pattern)
            date_matches_description = get_date_matches(description, pattern=pattern)
            date_match = ""
            if len(date_matches_title) > 0:
                date_match = date_matches_title[0]
            if len(date_matches_description) > 0:
                if len(date_matches_description[0]) > len(date_match):
                    date_match = date_matches_description[0]
            if date_match:
                if i == 1:
                    date_match_formatted = format_date(date_match, format_type=3)
                elif i == 2:
                    date_match_formatted = format_date(date_match, format_type=1)
                elif i == 3:
                    date_match_formatted = format_date(date_match, format_type=2)
            if date_match != "" and len(date_match) > len(start):
                start = date_match_formatted
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            break
        link = "https://www.hlnug.de" + body_element.find("a").get("href")
        location = ""
        if options.get("parse_details_pages", True):
            description = parse_details_page(link)

        event = Event(
            title=title,
            start=start,
            location=location,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events
