import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="news-text-wrap")
    if not content_div:
        return "", "", "", "", ""
    
    paragraphs = content_div.find_all('p')
    topic = ""
    target_group = ""
    location = ""
    actor = ""
    for paragraph in paragraphs:
        if paragraph.find('strong') and 'Schwerpunkte' in paragraph.find('strong').text:
            text = paragraph.get_text()
            if "Zielgruppen:" in text and "Schwerpunkte:" in text:
                topic = text.split("Zielgruppen:")[0].split("Schwerpunkte:")[1]
                target_group = text.split("Zielgruppen:")[1]
            else:
                topic = text.split("Schwerpunkte:")[1]
        if paragraph.find('strong') and 'Zielgruppen' in paragraph.find('strong').text:
            text = paragraph.get_text()
            if "Schwerpunkte:" in text:
                target_group = text.split("Schwerpunkte:")[1]
            else:
                target_group = text.split("Zielgruppen:")[1]
        if paragraph.find('strong') and 'Ort' in paragraph.find('strong').text:
            location = paragraph.get_text().split("Ort:")[1]
            if normalize_whitespace(location) == "":
                location = paragraph.find_next_sibling('p').get_text()
        if paragraph.find('strong') and 'Veranstalter' in paragraph.find('strong').text:
            actor = paragraph.get_text().split("Veranstalter:")[1]
            if normalize_whitespace(actor) == "":
                actor = paragraph.find_next_sibling('p').get_text()
    topic = normalize_whitespace(topic)
    target_group = normalize_whitespace(target_group)
    location = normalize_whitespace(location)
    actor = normalize_whitespace(actor)

    description = normalize_whitespace(content_div.get_text())
    return topic, actor, location, target_group, description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="news").find_all("li")
    events = []
    today = today_date_string()
    for element in event_elements:
        # Get the dates of the event and skip it if it's before the cut-off date
        date_element = element.find("time")
        start = date_element.get_text(strip=True) if date_element else ""

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            continue

        a_element = element.find("a")
        title = a_element.get_text(strip=True) if a_element else ""
        link = "https://tlubn.thueringen.de/" + a_element["href"] if a_element else ""
        location = ""
        timeframe = ""
        description = ""
        topic = ""
        actor = ""
        target_group = ""
        if options.get("parse_details_pages", True):
            topic, actor, location, target_group, description = parse_details_page(link)

        event = Event(
            title=title,
            start=start,
            timeframe=timeframe,
            location=location,
            topic=topic,
            actor=actor,
            target_group=target_group,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events
