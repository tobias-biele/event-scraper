import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("section", class_="cmp_content")
    topic = content_div.find("h2").get_text()
    timeframe_headline = content_div.find("h3", string="Beginn und Ende")
    timeframe = ""
    if timeframe_headline:
        timeframe_element = timeframe_headline.find_next_sibling("p")
        if timeframe_element:
            timeframe = normalize_whitespace(timeframe_element.get_text())
    location_headline = content_div.find("h3", string="Veranstaltungsort")
    location = ""
    if location_headline:
        location_element = location_headline.find_next_sibling("p")
        if location_element:
            location = normalize_whitespace(location_element.get_text())
    actor_headline = content_div.find("h3", string="Veranstalter")
    actor = ""
    if actor_headline:
        actor_element = actor_headline.find_next_sibling("p")
        if actor_element:
            actor = normalize_whitespace(actor_element.get_text())
    description = normalize_whitespace(content_div.get_text())
    return topic, timeframe, location, actor, description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    events = []
    skipped_count = 0
    today = today_date_string()
    year_sections = soup.find("div", class_="cmp_list_group").find_all("ul")
    for year_section in year_sections:
        event_elements = year_section.find_all("li")
        year = year_section.find_previous_sibling("h2").get_text()
        for element in event_elements:
            # Get the dates of the event and skip it if it's before the cut-off date
            date_text = element.find("small").get_text()
            month_digits = date_text.split(".")[-2]
            start = f'{date_text.split(".")[0]}.{month_digits}.{year}'
            end = "" if not "bis" in date_text else date_text.split("bis ")[1] + year

            if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
                skipped_count += 1
                continue

            title = element.find("a").get_text()
            link = "https://www.lfu.bayern.de/" + element.find("a")["href"]
            location_element = element.find("div", class_="text-end")
            location = ""
            if location_element:
                location = location_element.find("small").get_text()

            timeframe = ""
            description = ""
            actor = ""
            topic = ""
            if options.get("parse_details_pages", True):
                topic, timeframe, location, actor, description = parse_details_page(link)

            event = Event(
                title=title,
                start=start,
                end=end,
                timeframe=timeframe,
                location=location,
                actor=actor,
                topic=topic,
                link=link,
                added=today,
                description=description,
            )
            events.append(event)
    return events, f"({skipped_count} skipped)"
