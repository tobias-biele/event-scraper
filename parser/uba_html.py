import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

from event import Event
from .utils import today_date_string, normalize_whitespace, unformat_date

def parse_details_page(url):
    details_page = requests.get(url)
    details_soup = BeautifulSoup(details_page.content, "html.parser")
    content_div = details_soup.find("div", class_="article-content")
    description = normalize_whitespace(content_div.get_text())
    return description

def parse(url, options):
    # Initialize a headless web browser
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    driver.get(url)

    # Simulate scrolling to load additional content
    for _ in range(5):  # Adjust the number of scrolls as needed
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)  # Wait for new content to load (adjust as needed)

    # Get the updated page source after scrolling
    updated_page_source = driver.page_source
    soup = BeautifulSoup(updated_page_source, 'html.parser')

    # Parse the events
    event_title_elements = soup.find_all("h5")
    events = []
    today = today_date_string()
    for title_element in event_title_elements:
        # Get the dates of the event and skip it if it's before the cut-off date
        start = ""
        end = ""
        date_elements = title_element.find_previous_sibling().find_all("time")
        if len(date_elements) > 0:
            start = date_elements[0].text.strip()
        if len(date_elements) > 1:
            end = date_elements[1].text.strip()
        if start != None and start != "" and options.get("cut_off_date", None) and unformat_date(start) < options["cut_off_date"]:
            continue
        
        title = title_element.text.strip()
        description_element = title_element.find_next_sibling("p")
        link = "https://www.umweltbundesamt.de" + description_element.find("a")["href"]

        description = description_element.text.strip()
        if options.get("parse_details_pages", True):
            description = parse_details_page(link)

        event = Event(
            title=title,
            start=start,
            end=end,
            link=link,
            added=today,
            description=description,
        )
        events.append(event)
    driver.quit()
    return events
