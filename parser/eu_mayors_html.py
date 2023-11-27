import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    details_div = details_soup.find("div", id="event-details").find("div")
    practical_info_div = details_soup.find("div", id="event-practical-information").find("div")
    start = None
    end = None
    timeframe = None
    actor = None
    location = None
    description = None
    if details_div:
        description = normalize_whitespace(details_div.get_text(strip=True))
    if practical_info_div:
        where_dt = practical_info_div.find("dt", string="Where")
        if where_dt:
            location = normalize_whitespace(where_dt.find_next_sibling("dd").get_text(strip=True))
        when_dt = practical_info_div.find("dt", string="When")
        if when_dt:
            time_elements = when_dt.find_next_sibling("dd").find_all("time")
            if len(time_elements) == 2:
                start_str = time_elements[0].get_text(strip=True)
                end_str = time_elements[1].get_text(strip=True)
                start_split = start_str.split(", ")[0].split(" ")
                start_date_str = f"{start_split[1]} {start_split[2]} {start_split[3]}"
                start_time_str = start_str.split(", ")[1]
                end_split = end_str.split(", ")[0].split(" ")
                end_date_str = f"{end_split[1]} {end_split[2]} {end_split[3]}"
                end_time_str = end_str.split(", ")[1]
            if start_date_str == end_date_str or end_date_str == None:
                timeframe = f"{start_time_str} - {end_time_str}"
            else:
                start = f"{format_date(start_date_str, 6)} {start_time_str}"
                end = f"{format_date(end_date_str, 6)} {end_time_str}"
        organiser_dt = practical_info_div.find("dt", string="Organiser")
        if organiser_dt:
            actor = normalize_whitespace(organiser_dt.find_next_sibling("dd").get_text(strip=True))
                
    return description, start, end, timeframe, actor, location

def parse(url, options):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    event_elements = soup.find("div", class_="views-view-grid").find_all("div", class_="views-row")
    events = []
    skipped_count = 0
    today = today_date_string()
    for element in event_elements:
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""

        date_element = element.find("time")
        if date_element:
            day = date_element.find("span", class_="ecl-date-block__day").get_text(strip=True)
            if "-" in day:
                day_start = day.split("-")[0]
                day_end = day.split("-")[1]
                start = format_date(f"{day_start} {month} {year}", 5)
                end = format_date(f"{day_end} {month} {year}", 5)
            else:
                month = date_element.find("abbr", class_="ecl-date-block__month").get_text(strip=True)
                year = date_element.find("span", class_="ecl-date-block__year").get_text(strip=True)
                start = format_date(f"{day} {month} {year}", 5)

        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            skipped_count += 1
            continue

        title = ""
        link = ""
        location = ""
        timeframe = ""

        description_element = element.find("div", class_="ecl-content-block__description")
        if description_element:
            location_element = description_element.find("li")
            if location_element:
                location = location_element.get_text(strip=True)

        title_element = element.find("h1")
        if title_element:
            title = title_element.get_text(strip=True)
            link = "https://eu-mayors.ec.europa.eu" + title_element.find("a")["href"]

        description = ""
        actor = ""
        if options.get("parse_details_pages", True):
            d, s, e, t, a, l = parse_details_page(link)
            if d:
                description = d
            if s:
                start = s
            if e:
                end = e
            if t:
                timeframe = t
            if a:
                actor = a
            if l:
                location = l

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
