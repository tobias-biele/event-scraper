import feedparser
import re
import requests
from datetime import date, datetime

import locale
locale.setlocale(locale.LC_TIME, 'de_DE.ISO8859-1')

def fetch_and_parse_rss_feed(feed_url):
    try:
        response = requests.get(feed_url)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        return feed.entries
    except requests.RequestException as e:
        print(f"Error fetching feed from {feed_url}: {e}")
        return []

def today_date_string(reverse_format=False):
    if reverse_format:
        return date.today().strftime("%Y-%m-%d")
    else:
        return date.today().strftime("%d.%m.%Y")

def today_date():
    return date.today()

def format_date(str, format_type=0):
    if format_type == 0:
        # format: 2021-12-01
        date = datetime.strptime(str, "%Y-%m-%d")
        return date.strftime("%d.%m.%Y")
    elif format_type == 1:
        # format: 01. Dezember 2021
        date_format = "%d. %B %Y"
        date = datetime.strptime(str, date_format)
        return date.strftime("%d.%m.%Y")
    elif format_type == 2:
        # format: 01. Dezember
        date_format = "%d. %B"
        date = datetime.strptime(str, date_format)
        return date.strftime("%d.%m")
    elif format_type == 3:
        # format: 01.12.21
        date = datetime.strptime(str, "%d.%m.%y")
        return date.strftime("%d.%m.%Y")
    elif format_type == 4:
        # format 01. Dez
        str = str.replace("Jan", "Januar")
        str = str.replace("Feb", "Februar")
        str = str.replace("Mär", "März")
        str = str.replace("Apr", "April")
        str = str.replace("Jun", "Juni")
        str = str.replace("Jul", "Juli")
        str = str.replace("Aug", "August")
        str = str.replace("Sep", "September")
        str = str.replace("Okt", "Oktober")
        str = str.replace("Nov", "November")
        str = str.replace("Dez", "Dezember")
        return format_date(str, 2)
    elif format_type == 5:
        # format 01 Dec 2021
        str = str[:2] + "." + str[2:] # insert dot after day
        str = str.replace("Jan", "Januar")
        str = str.replace("Feb", "Februar")
        str = str.replace("Mar", "März")
        str = str.replace("Apr", "April")
        str = str.replace("Jun", "Juni")
        str = str.replace("Jul", "Juli")
        str = str.replace("Aug", "August")
        str = str.replace("Sep", "September")
        str = str.replace("Oct", "Oktober")
        str = str.replace("Nov", "November")
        str = str.replace("Dec", "Dezember")
        return format_date(str, 1)
    elif format_type == 6:
        # format 01 December 2021
        str = str[:2] + "." + str[2:] # insert dot after day
        str = str.replace("January", "Januar")
        str = str.replace("February", "Februar")
        str = str.replace("March", "März")
        str = str.replace("June", "Juni")
        str = str.replace("July", "Juli")
        str = str.replace("October", "Oktober")
        str = str.replace("December", "Dezember")
        return format_date(str, 1)
    else:
        print("Unknown date format type")
        return None
    
def unformat_date(str):
    # Cut off time if present
    str = str.split(" ")[0]
    date = datetime.strptime(str, "%d.%m.%Y")
    return date.strftime("%Y-%m-%d")

def get_date_matches(text, pattern=r'(\d{2}.\d{2}.\d{4})'):
    date_pattern = pattern
    return re.findall(date_pattern, text)

def get_year_matches(text):
    year_pattern = r'(\d{4})'
    return re.findall(year_pattern, text)

def get_time_matches(text):
    time_pattern = r'(\d{2}:\d{2})'
    return re.findall(time_pattern, text)

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()
