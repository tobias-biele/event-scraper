import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, get_date_matches, get_time_matches, unformat_date

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="liste").find_all("div", class_="item")
    events = []
    skipped_count = 0
    today = today_date_string()
    for event_element in event_elements:
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""

        date_matches = get_date_matches(event_element.find("div", class_="leftTitle").get_text())
        if date_matches:
            start = date_matches[0]
            if len(date_matches) > 1:
                end = date_matches[1]

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        title = ""
        title_element = event_element.find("div", class_="title")
        if title_element:
            title = title_element.get_text(strip=True)
        location_element = event_element.find("div", class_="location")
        location = ""
        if location_element:
            location = location_element.get_text(strip=True)

        actor = ""
        table_element = event_element.find("table")
        actor_label_td = table_element.find("td", class_="label", string="Veranstalter:")
        if actor_label_td:
            actor = actor_label_td.find_next_sibling("td").get_text(strip=True)

        location_label_td = table_element.find("td", class_="label", string="Veranstaltungsort:")
        if location_label_td:
            location = location_label_td.find_next_sibling("td").get_text()

        timeframe = ""
        begin_label_td = table_element.find("td", class_="label", string="Beginn:")
        end_label_td = table_element.find("td", class_="label", string="Ende:")
        if begin_label_td:
            start_date = get_date_matches(begin_label_td.find_next_sibling("td").get_text(strip=True))
            start_time = get_time_matches(begin_label_td.find_next_sibling("td").get_text(strip=True))
            if start_date:
                start = start_date[0]
        if end_label_td:
            end_date = get_date_matches(end_label_td.find_next_sibling("td").get_text(strip=True))
            end_time = get_time_matches(end_label_td.find_next_sibling("td").get_text(strip=True))
        if start_date and end_date:
            if start_time and end_time and start_date == end_date:
                start = start_date[0]
                end = end_date[0]
                timeframe = f"{start_time[0]} - {end_time[0]}"
            elif start_time and end_time and start_date != end_date:
                start = f"{start_date[0]} {start_time[0]}"
                end = f"{end_date[0]} {end_time[0]}"
            else:
                start = start_date[0]
                end = end_date[0]

        link = ""
        link_label_td = table_element.find("td", class_="label", string="Internet:")
        if link_label_td:
            link = link_label_td.find_next_sibling("td").find("a").get("href")

        description = ""
        description_element = table_element.find("td", class_="first")
        if description_element:
            description = description_element.get_text(strip=True)

        event = Event(
            title=title,
            start=start,
            end=end,
            timeframe=timeframe,
            location=location,
            actor=actor,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events, f"({skipped_count} skipped)"
