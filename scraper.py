import importlib
from actors import actors
from excel import create_sheet

def run(parse_details_pages=False, cut_off_date=None):
    """
    Run the scraper.

    :param parse_details_pages: If True, the scraper will parse details pages. This might take a while.
    :param cut_off_date: All events before this date will be ignored.
    """
    options = {
        "parse_details_pages": parse_details_pages,
        "cut_off_date": cut_off_date,
    }
    print("Starting...")
    if options["parse_details_pages"]:
        print("The scraper will parse details pages for individual events. This might take a while.")
    else:
        print("The scraper will not parse details pages.")

    xlsx_rows = []
    for actor_name, actor_config in actors.items():
        try:
            parser_module = importlib.import_module(actor_config["parser_module"])
            parse = parser_module.parse
            events = parse(actor_config["url"], options)
            print("Scraped", len(events), "events from", actor_name)
            xlsx_rows.extend([event.to_xlsx_row() for event in events])
        except ImportError as e:
            print(f"Error importing {actor_config['parser_module']}: {e}")
        except Exception as e:
            print(f"Error parsing {actor_name}: {e}")
    create_sheet(xlsx_rows)

run(parse_details_pages=True)