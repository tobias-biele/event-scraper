import feedparser
import re
import requests
from datetime import date, datetime

def fetch_and_parse_rss_feed(feed_url):
    try:
        response = requests.get(feed_url)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        return feed.entries
    except requests.RequestException as e:
        print(f"Error fetching feed from {feed_url}: {e}")
        return []

def today_date():
    return date.today().strftime("%d.%m.%Y")

def format_date(str, format_type=0):
    if format_type == 0:
        date = datetime.strptime(str, "%Y-%m-%d")
        return date.strftime("%d.%m.%Y")
    elif format_type == 1:
        date_format = "%d. %B %Y"
        date = datetime.strptime(str, date_format)
        return date.strftime("%d.%m.%Y")
    else:
        print("Unknown date format type")
        return str

def get_date_matches(text):
    date_pattern = r'(\d{2}.\d{2}.\d{4})'
    return re.findall(date_pattern, text)

def get_time_matches(text):
    time_pattern = r'(\d{2}:\d{2})'
    return re.findall(time_pattern, text)

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()