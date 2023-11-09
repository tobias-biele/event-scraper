import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date, get_date_matches, get_time_matches, normalize_whitespace

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", id="block-content")
    actor = ""
    target_group = ""
    description = ""

    actor_div = content_div.find("div", class_="field--name-field-event-organiser")
    if actor_div:
        actor = actor_div.find("div", class_="field__item").text.strip()
    target_group_div = content_div.find("div", class_="field--name-field-event-participants")
    if target_group_div:
        target_group = target_group_div.find("div", class_="field__item").text.strip()

    abstract_div = content_div.find("div", class_="field--name-field-abstract")
    description_div = content_div.find("div", class_="field--name-field-description")
    if abstract_div:
        description += normalize_whitespace(abstract_div.get_text())
    elif description_div:
        description += normalize_whitespace(description_div.get_text())
    
    return actor, target_group, description

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_element = soup.find("div", id="results-events").find_all("article")
    events = []
    today = today_date()
    for element in event_element:
        a_element = element.find("a")
        title = a_element.find("span").text.strip()
        link = "https://www.bfn.de" + a_element["href"]
        location = element.find("div", class_="field--name-field-location").find("span").text.strip()
        start = ""
        end = ""
        timeframe = ""
        start_div = element.find("div", class_="field--name-field-event-startdate")
        end_div = element.find("div", class_="field--name-field-event-enddate")
        if start_div:
            start_date = get_date_matches(start_div.find("div", class_="field__item").text.strip())
            start_time = get_time_matches(start_div.find("div", class_="field__item").text.strip())
            if start_date:
                start = start_date[0]
            if start_time:
                start += " " + start_time[0]
        if end_div:
            end_date = get_date_matches(end_div.find("div", class_="field__item").text.strip())
            end_time = get_time_matches(end_div.find("div", class_="field__item").text.strip())
            if end_date:
                end = end_date[0]
            if end_time:
                end += " " + end_time[0]

        description = element.find("div", class_="field--name-field-abstract").text.strip()
        actor = ""
        target_group = ""
        if options.get("parse_details_pages", True):
            actor, target_group, description = parse_details_page(link)
        
        event = Event(
            title=title,
            start=start,
            end=end,
            timeframe=timeframe,
            actor=actor,
            target_group=target_group,
            location=location,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    return events
