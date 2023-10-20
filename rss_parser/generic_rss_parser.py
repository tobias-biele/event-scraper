import feedparser
import requests

def fetch_and_parse_feed(feed_url):
    try:
        response = requests.get(feed_url)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        return feed.entries
    except requests.RequestException as e:
        print(f"Error fetching feed from {feed_url}: {e}")
        return []

def parse(feed_url):
    parsed_data = fetch_and_parse_feed(feed_url)
    return parsed_data