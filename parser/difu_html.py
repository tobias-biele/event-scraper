import requests
from bs4 import BeautifulSoup
from .utils import get_date_matches

def parse_details_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Find dates
    start = ""
    end = ""
    date_div = soup.find_all("div", class_="veranstaltung__field-datum-start")
    if len(date_div) > 0:
        date_matches = get_date_matches(date_div[0].text)
        if len(date_matches) == 1:
            start = date_matches[0]
        elif len(date_matches) == 2:
            start = date_matches[0]
            end = date_matches[1]
    # Find timeframe
    timeframe = ""
    timeframe_div = soup.find_all("div", class_="veranstaltung__field-oeffnungszeiten")
    if len(timeframe_div) > 0:
        timeframe = timeframe_div[0].text
    # Find location
    location = ""
    location_label_div = soup.find("div", class_="sidebar-heading", string=lambda text: text and text.strip() == "Ort")
    location_div = None
    if location_label_div:
        location_div = location_label_div.find_next_sibling('div')
    if location_div:
        location_elements = location_div.find("div").find_all("div")
        location = "\n".join(element.get_text(strip=True) for element in location_elements)
    return {
        "start": start,
        "end": end,
        "timeframe": timeframe,
        "location": location,
    }