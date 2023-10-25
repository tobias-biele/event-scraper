import requests
from bs4 import BeautifulSoup
from .utils import get_date_matches

def parse_details_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Find date
    title_headline = soup.find_all('h1')[0]
    subtitle = title_headline.find_next_sibling('span')
    date_matches = get_date_matches(subtitle.text)
    if len(date_matches) > 0:
        date = date_matches[0]
    # Find timeframe
    time_label_divs = soup.find_all('div', string=lambda text: text and 'zeit' in text.lower())
    time_div = None
    if len(time_label_divs) > 0:
        time_label_div = time_label_divs[0]
        time_div = time_label_div.find_next_sibling('div')

    return {
        "date": date,
        "timeframe": time_div.text.strip() if time_div else ""
    }