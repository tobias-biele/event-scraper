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

    return {
        "start": start,
        "end": end,
        "timeframe": timeframe
    }