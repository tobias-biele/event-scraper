import feedparser
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
