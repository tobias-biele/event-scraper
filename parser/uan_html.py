import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, today_date, unformat_date, get_year_matches

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    events_section_headings = soup.find("article", class_="content").find_all("div", class_="bg-white-start")
    events = []
    today = today_date_string()
    current_year = today_date().year
    current_month = 0 # Start at 0 to indicate that no month has been set yet. The page might contain outdated events from previous month.
    for heading_element in events_section_headings:
        heading = heading_element.find("h2").get_text(strip=True)
        actor = ""
        topic = ""
        if heading.startswith("Veranstaltungen der UAN"):
            actor = "UAN"
        elif heading.startswith("Weitere Veranstaltungshinweise"):
            topic = heading.split(": ")[1].strip()

        heading_years = get_year_matches(heading)
        if len(heading_years) > 0:
            current_year = int(heading_years[0])

        event_elements = heading_element.find_next_sibling("div", class_="bg-white-divider").find_all("div", class_="article")
                                                                                             
        for event_element in event_elements:
            # Get the dates of the event and skip it if it's before the cut-off date
            date_text = event_element.find("time").get("datetime")
            day = int(date_text.split("|")[0].strip())
            month = int(date_text.split("|")[1].strip())
            previous_month = current_month
            if previous_month > month:
                current_year += 1
            current_month = month
            start = f"{day:02d}.{month:02d}.{current_year}" # Pad day and month with zeros
        
            if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
                continue

            title_element = event_element.find("h3")
            title = title_element.get_text(strip=True)
            link = title_element.find("a").get("href")
            if link.startswith("/"):
                link = "https://www.uan.de" + link
            if actor == "UAN":
                topic_element = event_element.find("span", class_="news-list-category")
                if topic_element:
                    topic = topic_element.get_text().split("|")[1].split("|")[0].strip()

            description = ""
            description_element = event_element.find("p")
            if description_element:
                description = description_element.get_text(strip=True)

            event = Event(
                title=title,
                start=start,
                link=link,
                actor=actor,
                topic=topic,
                added=today,
                description=description,
            )
            events.append(event)
    return events
