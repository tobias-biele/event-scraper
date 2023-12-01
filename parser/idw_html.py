import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, normalize_whitespace, get_date_matches, get_time_matches, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="blueline-top")
    description = ""
    start = ""
    end = ""
    timeframe = ""
    location = ""
    target_group = ""
    topic = ""
    actor = ""
    if content_div:
        termin_element = content_div.find("p", string=lambda text: text and 'termin' in text.lower())
        date_element = termin_element.parent.find_next_sibling().find("span")
        if date_element:
            date_string = date_element.get_text()
            date_matches = get_date_matches(date_string)
            time_matches = get_time_matches(date_string)
            if len(date_matches) == 2:
                start = date_matches[0]
                end = date_matches[1]
                if len(time_matches) == 2:
                    start += " " + time_matches[0]
                    end += " " + time_matches[1]
            elif len(date_matches) == 1:
                start = date_matches[0]
                if len(time_matches) == 2:
                    timeframe = time_matches[0] + " - " + time_matches[1]
        location_element = content_div.find("p", string=lambda text: text and 'veranstaltungsort' in text.lower())
        if location_element:
            location = location_element.parent.find_next_sibling().get_text()
        target_group_element = content_div.find("p", string=lambda text: text and 'zielgruppe' in text.lower())
        if target_group_element:
            target_group = target_group_element.parent.find_next_sibling().get_text()
        topic_element = content_div.find("p", string=lambda text: text and 'sachgebiete' in text.lower())#
        if topic_element:
            topic = topic_element.parent.find_next_sibling().get_text()
        actor_element = content_div.find("p", string=" ")
        if actor_element:
            actor = actor_element.parent.find_next_sibling().get_text()
        description_element = content_div.find("h5", class_="subheader")
        if description_element:
            description = normalize_whitespace(description_element.find_next_sibling().get_text())
    return description, start, end, timeframe, location, target_group, topic, actor

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="blueline-top").find_all("div", class_="row")
    events = []
    skipped_count = 0
    today = today_date_string()
    for event_element in event_elements:
        event_row_columns = event_element.find_all("div")
        date_location_column = event_row_columns[0]
        title_column = event_row_columns[1]

        # Get the dates of the event and skip it if it's before the cut-off date
        date_matches = get_date_matches(date_location_column.get_text())
        start = ""
        end = ""
        if len(date_matches) > 0:
            start = date_matches[0]
        if len(date_matches) > 1:
            end = date_matches[1]
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        title = ""
        link = ""
        if title_column:
            title = title_column.get_text(strip=True)
            link = title_column.find("a")["href"]
        if len([e for e in events if e.title == title]) > 0:
            # Skip duplicates
            continue
        try:
            location = date_location_column.find("br").find_next_sibling().get_text()
        except:
            location = ""

        timeframe = ""
        description = ""
        target_group = ""
        topic = ""
        actor = ""
        if options.get("parse_details_pages", True):
            description, start_details, end_details, timeframe, location, target_group, topic, actor = parse_details_page(link)
            if start_details:
                start = start_details
            if end_details:
                end = end_details

        event = Event(
            title=title,
            start=start,
            end=end,
            timeframe=timeframe,
            location=location,
            target_group=target_group,
            topic=topic,
            actor=actor,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events, f"({skipped_count} skipped [including duplicates])"
