import requests
from bs4 import BeautifulSoup
from event import Event
from .utils import today_date_string, format_date, normalize_whitespace, get_date_matches, get_time_matches, unformat_date, get_year_matches

def parse_details_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    } # BUND blocks standard requests from the requests library, therefore we need to set a user agent
    details_page = requests.get(url, headers=headers)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="das-hier-ist-column-main")
    actor = "BUND"
    if content_div:
        description = normalize_whitespace(content_div.get_text())
    else:
        description = normalize_whitespace(details_soup.get_text())
    sidebar_div = details_soup.find("div", class_="m-sidebar-content")
    if sidebar_div:
        p_veranstalter = sidebar_div.find("p", class_="rte-paragraph", string=lambda text: "veranstalter" in text.lower())
        if p_veranstalter and p_veranstalter.find_next_sibling() is not None:
            actor_text = p_veranstalter.find_next_sibling().get_text(strip=True)
            actor = normalize_whitespace(actor_text)
    return description, actor

def parse(url, options):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    } # BUND blocks standard requests from the requests library, therefore we need to set a user agent
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    pagination_list = soup.find("ul", class_="m-navigation-pagination--list")
    last_page = pagination_list.find("li", class_="last")
    last_page_page_url = "https://bund.net" + last_page.find("a")["href"]
    url_without_page_number = last_page_page_url.split("currentPage%5D=")[0] + "currentPage%5D="
    number_of_pages = last_page.get_text(strip=True)

    events = []
    skipped_count = 0
    today = today_date_string()
    for page_number in range(1, int(number_of_pages) + 1):
        page_url = url_without_page_number + str(page_number)
        page = requests.get(page_url, headers=headers)
        page_soup = BeautifulSoup(page.content, "html.parser")

        event_elements = page_soup.find_all("article", class_="m-content-dashboardbox")
        for element in event_elements:
            p_elements = element.find_all("p", class_="rte-paragraph")         
            # Get the dates of the event and skip it if it's before the cut-off date
            start = ""
            end = ""
            timeframe = ""
            if len(p_elements) > 0:
                malformed_date = False
                date_text = p_elements[0].get_text(strip=True)
                if " um " in date_text:
                    date = normalize_whitespace(date_text.split(" um ")[0])
                    timeframe = normalize_whitespace(date_text.split(" um ")[1])
                    if " | " in timeframe:
                        timeframe = timeframe.split(" | ")[0]
                elif " | " in date_text:
                    date = normalize_whitespace(date_text.split(" | ")[0])
                else:
                    date = normalize_whitespace(date_text)

            if " - " in date:
                # string contains start and end date
                # case 1: same month. Example: 01. - 02. Dezember 2023
                # case 2: different month, same year. Example: 01. Nov - 01. Dezember 2023
                # case 3: different month, different year. Example: 01. Dez 2023 - 01. Januar 2024
                try:
                    end_text = date.split(" - ")[1]
                    _, end_month, end_year = end_text.split(" ")
                    start_text = date.split(" - ")[0]
                    if len(start_text) == 3:
                        # case 1
                        start_text = start_text + " " + end_month + " " + end_year
                        start = format_date(start_text)
                    else:
                        start_text_split = start_text.split(" ")
                        if len(start_text_split) == 2:
                            # case 2
                            start_text = start_text + " " + end_year
                            start = format_date(start_text)
                    start = format_date(start_text)
                    end = format_date(end_text)
                except Exception as e:
                    malformed_date = True
            else:
                try:
                    start = format_date(date)
                except:
                    malformed_date = True
            
            if not malformed_date:
                if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
                    skipped_count += 1
                    continue

            title = ""
            title_headline = element.find("h1")
            if title_headline:
                title = title_headline.get_text(strip=True)
            link = element.find("a")["href"]
            if link.startswith("/"):
                link = "https://bund.net" + link
            location = ""
            if len(p_elements) > 1:
                p_location = p_elements[1]
                location = p_location.get_text(strip=True).split("Ort: ")[1]

            description = ""
            actor = "BUND"
            if options.get("parse_details_pages", True):
                description, actor = parse_details_page(link)

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
