import requests
from bs4 import BeautifulSoup
from .utils import get_date_matches, get_time_matches, normalize_whitespace

def parse_details_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Find dates and timeframe
    start = ""
    end = ""
    timeframe = ""
    description = ""
    time_divs = soup.find_all("time")
    if len(time_divs) > 0:
        start_date_match = get_date_matches(time_divs[0].text)
        start_time_match = get_time_matches(time_divs[0].text)
        if len(start_date_match) > 0:
            start = start_date_match[0]
        if len(start_time_match) > 0:
            timeframe = start_time_match[0]
    if len(time_divs) > 1:
        end_date_match = get_date_matches(time_divs[1].text)
        end_time_match = get_time_matches(time_divs[1].text)
        if len(end_date_match) > 0:
            end = end_date_match[0]
        if len(end_time_match) > 0:
            timeframe += " - " + end_time_match[0]

    # Find location
    location = ""
    location_headline = soup.find("h2", string="Veranstaltungsort")
    if location_headline:
        p_element = location_headline.next_sibling.next_sibling
        address_lines = [line.strip() for line in p_element.get_text().split('\n') if line.strip()]
        location = "\n".join(address_lines)
    
    content_div = soup.find("div", class_="content")
    if content_div:
        description = normalize_whitespace(content_div.get_text())

    return {
        "start": start,
        "end": end,
        "timeframe": timeframe,
        "location": location,
        "description": description,
    }
