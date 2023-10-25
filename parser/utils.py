import feedparser
import re
import requests
from datetime import date

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

def get_date_matches(text):
    date_pattern = r'(\d{2}.\d{2}.\d{4})'
    return re.findall(date_pattern, text)