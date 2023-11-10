import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, get_date_matches, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("article", class_="jki-event")
    description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all elements whose id attribute starts with "event-"
    elements_with_event_id = soup.find_all(lambda tag: tag.get('id', '').startswith('event-'))

    events = []
    today = today_date_string()
    for event_element in elements_with_event_id:
        # Get the dates of the event and skip it if it's before the cut-off date (dates are also scraped from the details page, if the option is set)
        start = ""
        end = ""
        dates_text = event_element.find('time').text.strip()
        date_matches = get_date_matches(dates_text)
        if len(date_matches) == 1:
            start = date_matches[0]
        elif len(date_matches) == 2:
            start, end = date_matches

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            continue

        title = event_element.find('h2').text.strip()
        institution = event_element.find("span", class_="jki-event__header__location").text
        link = 'https://www.julius-kuehn.de'+event_element.get('href')
        description = ""

        location = ""
        location_element = event_element.find("span", class_="jki-event__header__location")
        if location_element:
            location = location_element.text.strip()

        if options.get("parse_details_pages", True):
            # Get dates including start and end time from details page
            details_page = requests.get(link)
            details_soup = BeautifulSoup(details_page.content, "html.parser")
            table = details_soup.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    th = row.find('th', class_='jki-info-table__label')
                    td = row.find('td', class_='jki-info-table__content')
                    if th and td and "Beginn" in th.get_text():
                        start = td.text.strip().replace('. ', '.')
                    if th and td and "Ende" in th.get_text():
                        end = td.text.strip().replace('. ', '.')
            
            # Get description from details page
            description = parse_details_page(link)

        event = Event(
            title=title,
            actor=institution,
            start=start,
            end=end,
            location=location,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events
