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
        # format: 2021-01-01
        date = datetime.strptime(str, "%Y-%m-%d")
        return date.strftime("%d.%m.%Y")
    elif format_type == 1:
        # format: 01. Januar 2021
        date_format = "%d. %B %Y"
        date = datetime.strptime(str, date_format)
        return date.strftime("%d.%m.%Y")
    elif format_type == 2:
        # format: 01. Januar
        date_format = "%d. %B"
        date = datetime.strptime(str, date_format)
        return date.strftime("%d.%m")
    elif format_type == 3:
        # format: 01.01.21
        date = datetime.strptime(str, "%d.%m.%y")
        return date.strftime("%d.%m.%Y")
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

def get_time_matches(text):
    time_pattern = r'(\d{2}:\d{2})'
    return re.findall(time_pattern, text)

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()
