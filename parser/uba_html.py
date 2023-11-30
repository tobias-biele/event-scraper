import requests
from bs4 import BeautifulSoup

from event import Event
from .utils import today_date_string, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="article-content")
    description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    events = []
    for page_number in range(1, 11):
        paginated_url = f'{url}?page={page_number}'
        page = requests.get(paginated_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Parse the events
        event_title_elements = soup.find_all("h5")
        if len(event_title_elements) == 0:
            break
        skipped_count = 0
        today = today_date_string()
        for title_element in event_title_elements:
            if len([e for e in events if e.title == title_element.text.strip()]) > 0:
                # Skip duplicates which can occur due to pagination
                continue

            # Get the dates of the event and skip it if it's before the cut-off date
            start = ""
            end = ""
            date_elements = title_element.find_previous_sibling().find_all("time")
            if len(date_elements) > 0:
                start = date_elements[0].text.strip()
            if len(date_elements) > 1:
                end = date_elements[1].text.strip()
            if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
                skipped_count += 1
                continue
            
            title = title_element.text.strip()
            description_element = title_element.find_next_sibling("p")
            link = "https://www.umweltbundesamt.de" + description_element.find("a")["href"]

            description = description_element.text.strip()
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
