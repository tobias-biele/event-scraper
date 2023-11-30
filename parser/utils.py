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

def today_date_string(reverse_format=False):
    if reverse_format:
        return date.today().strftime("%Y-%m-%d")
    else:
        return date.today().strftime("%d.%m.%Y")

def today_date():
    return date.today()

def replace_month_name_with_number(str):
    month = str.split(" ")[1]
    if month == "Januar" or month == "Jan" or month == "January":
        return str.replace(month, "01")
    elif month == "Februar" or month == "Feb" or month == "February":
        return str.replace(month, "02")
    elif month == "März" or month == "Mär" or month == "Mar" or month == "March":
        return str.replace(month, "03")
    elif month == "April" or month == "Apr":
        return str.replace(month, "04")
    elif month == "Mai" or month == "May":
        return str.replace(month, "05")
    elif month == "Juni" or month == "Jun" or month == "June":
        return str.replace(month, "06")
    elif month == "Juli" or month == "Jul" or month == "July":
        return str.replace(month, "07")
    elif month == "August" or month == "Aug":
        return str.replace(month, "08")
    elif month == "September" or month == "Sep":
        return str.replace(month, "09")
    elif month == "Oktober" or month == "Okt" or month == "Oct" or month == "October":
        return str.replace(month, "10")
    elif month == "November" or month == "Nov":
        return str.replace(month, "11")
    elif month == "Dezember" or month == "Dez" or month == "Dec" or month == "December":
        return str.replace(month, "12")
    else:
        print("Unknown month name:", month)
        return None

def format_date(str):
    """Converts a date string to the format dd.mm.yyyy:"""
    if re.match(r'\d{4}-\d{2}-\d{2}', str):
        # format: 2021-12-01
        date = datetime.strptime(str, "%Y-%m-%d")
        return date.strftime("%d.%m.%Y")
    
    # Add leading zero to day if necessary
    if (
        re.match(r'\d{1}\.\d{2}\.\d{2}', str) or 
        re.match(r'\d{1}\.\d{2}\.\d{4}', str) or
        re.match(r'\d{1} (\w+) \d{4}', str) or
        re.match(r'\d{1}\. (\w+) \d{4}', str) or
        re.match(r'\d{1} (\w+)', str) or
        re.match(r'\d{1}\. (\w+)', str)
    ):
        str = "0" + str
    
    if re.match(r'\d{2}\.\d{2}\.\d{2}$', str):
        # format: 01.12.21
        str = str[:6] + "20" + str[6:]
    if re.match(r'\d{2}\.\d{2}\ \d{4}', str):
        # format: 01.12 2021
        str = str.replace(" ", ".")
    if re.match(r'\d{2}\.\d{2}\.\d{4}', str):
        # format: 01.12.2021
        return str
    
    if re.match(r'\d{2} (\w+) \d{4}', str):
        # format: 01 Dezember/December/Dez/Dec 2021
        str = str[:2] + "." + str[2:]
    if re.match(r'\d{2}\. (\w+) \d{4}', str):
        # format: 01. Dezember/December/Dez/Dec 2021
        str = replace_month_name_with_number(str)
        date_format = "%d. %m %Y"
        date = datetime.strptime(str, date_format)
        return date.strftime("%d.%m.%Y")
    
    # No year given
    if re.match(r'\d{2} (\w+)', str):
        # format: 01 Dezember/December/Dez/Dec
        str = str[:2] + "." + str[2:]
    if re.match(r'\d{2}\. (\w+)', str):
        # format: 01. Dezember/December/Dez/Dec
        str = replace_month_name_with_number(str)
        date_format = "%d. %m"
        date = datetime.strptime(str, date_format)
        return date.strftime("%d.%m")
    
    print("Unknown date format", str)
    return str
    
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
