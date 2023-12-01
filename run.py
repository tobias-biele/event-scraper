from scraper import run
from parser.utils import today_date_string

# PARAMETER SECTION
# --------------------------------
DETAIL_SEITEN_SCRAPEN = True
MINDESTDATUM = "heute"
INCLUDE = None
EXCLUDE = None
# --------------------------------

if MINDESTDATUM == "heute":
    MINDESTDATUM = today_date_string(reverse_format=True)

run(parse_details_pages=DETAIL_SEITEN_SCRAPEN, cut_off_date=MINDESTDATUM, include=INCLUDE, exclude=EXCLUDE)