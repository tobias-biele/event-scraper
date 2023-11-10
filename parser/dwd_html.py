import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="body-text")
    description = ""
    if content_div:
        description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    event_element = soup.find("article", class_="article-full")
    if event_element:
        event_table_rows = event_element.find_all("tr")
    else:
        event_table_rows = soup.find_all("tr")
    events = []
    today = today_date_string()
    for element in event_table_rows:
        table_columns = element.find_all("td")
        if len(table_columns) < 4: # skip header row
            continue
        # Get the dates of the event and skip it if it's before the cut-off date
        start = table_columns[0].text.strip()
        end = table_columns[1].text.strip()
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            continue

        title = table_columns[2].text.strip()
        link = "https://www.dwd.de/" + table_columns[2].find("a")["href"]
        location = table_columns[3].text.strip()

        description = ""
        if options.get("parse_details_pages", True):
            description = parse_details_page(link)
        
        event = Event(
            title=title,
            start=start,
            end=end,
            location=location,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events
