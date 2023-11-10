import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, get_date_matches, get_time_matches, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="content")
    start = ""
    end = ""
    location = ""
    description = ""

    event_info_div = content_div.find("ul", class_="document-info--event")
    if event_info_div:
        event_info_items = event_info_div.find_all("li")
        if len(event_info_items) > 0:
            start = get_date_matches(event_info_items[0].get_text())[0] + " " + get_time_matches(event_info_items[0].get_text())[0]
        if len(event_info_items) > 1:
            end = get_date_matches(event_info_items[1].get_text())[0] + " " + get_time_matches(event_info_items[1].get_text())[0]
        if len(event_info_items) > 2:
            location = event_info_items[2].get_text().strip()

    description_div = content_div.find("div", class_="rich-text")
    if description_div:
        description += normalize_whitespace(description_div.get_text())
    
    return start, end, location, description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    event_elements = soup.find_all('li', class_='card-list-item')

    events = []
    today = today_date_string()

    for event_element in event_elements:
        # Get the dates of the event and skip it if it's before the cut-off date (dates are also scraped from the details page, if the option is set)
        date_element = event_element.find('p', class_='card-date')
        dates = get_date_matches(date_element.text)
        start = dates[0] if len(dates) > 0 else ""
        end = dates[1] if len(dates) > 1 else ""
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            continue

        title = event_element.find('a', class_="card-link").find("strong").text.strip()
        link = "https://bmdv.bund.de/" + event_element.find("a")['href']
        location = ""
        location_element = event_element.find('p', class_='card-location')
        if location_element:
            location = location_element.text.strip().replace("Ort:  ", "")

        description = ""
        if options["parse_details_pages"]:
            start, end, location, description = parse_details_page(link)
            if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
                continue

        event = Event(
            title=title,
            start=start,
            end=end,
            actor="Bundesministerium für Digitales und Verkehr",
            location=location,
            link=link,
            added=today,
            description=description
        )
        events.append(event)
    return events
