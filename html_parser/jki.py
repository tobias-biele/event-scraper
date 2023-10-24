import re
import requests
from bs4 import BeautifulSoup
from datetime import date
from event import Event

def parse(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all elements whose id attribute starts with "event-"
    elements_with_event_id = soup.find_all(lambda tag: tag.get('id', '').startswith('event-'))

    events = []
    today = date.today().strftime("%d.%m.%Y")
    date_pattern = r'(\d{2}.\d{2}.\d{4})'
    for event_element in elements_with_event_id:
        title = event_element.find('h2').text.strip()
        institution = event_element.find("span", class_="jki-event__header__location").text
        link = 'https://www.julius-kuehn.de'+event_element.get('href')
        
        # Extract the dates (as backup in case the details page is not available)
        timeframe = event_element.find('time').text.strip()
        start = ""
        end = ""
        date_matches = re.findall(date_pattern, timeframe)
        if len(date_matches) == 1:
            start = date_matches[0]
        elif len(date_matches) == 2:
            start, end = date_matches

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
                    start = td.text.strip()
                if th and td and "Ende" in th.get_text():
                    end = td.text.strip()

        event = Event(
            title=title,
            actor=institution,
            start=start,
            end=end,
            link=link,
            added=today,
        )
        events.append(event)
    return events
