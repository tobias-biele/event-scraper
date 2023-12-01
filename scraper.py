import importlib
from actors import actors
from event import Event
from excel import create_sheet
from parser.utils import today_date_string

def run(parse_details_pages=False, cut_off_date=None, include=None, exclude=None):
    """
    Run the scraper.

    :param parse_details_pages: If True, the scraper will parse details pages. This might take a while.
    :param cut_off_date: All events before this date will be ignored.
    :param include: Only scrape actors whose names are in this list.
    :param exclude: Do not scrape actors whose names are in this list.
    """
    options = {
        "parse_details_pages": parse_details_pages,
        "cut_off_date": cut_off_date,
    }
    if include:
        include = [actor.lower() for actor in include]
        print("Include list provided. The scraper will only scrape the following actors:", include)
    if exclude:
        exclude = [actor.lower() for actor in exclude]
        print("Exclude list provided. The scraper will not scrape the following actors:", exclude)
    print("Starting...")
    if options["parse_details_pages"]:
        print("The scraper will parse details pages for individual events. This might take a while.")
    else:
        print("The scraper will not parse details pages.")

    xlsx_rows = []
    for actor_name, actor_config in actors.items():
        if include and actor_name not in include:
            print("Skipping", actor_name, "because it is not in the include list.")
            continue
        if exclude and actor_name in exclude:
            print("Skipping", actor_name, "because it is in the exclude list.")
            continue
        try:
            parser_module = importlib.import_module(actor_config["parser_module"])
            parse = parser_module.parse
            events, skipped_message = parse(actor_config["url"], options)
            for event in events:
                event.origin = actor_name
            output_message = f"Scraped {len(events)} events from {actor_name} {skipped_message}"
            print(output_message)
            xlsx_rows.extend([event.to_xlsx_row() for event in events])
        except ImportError as e:
            print(f"Error importing {actor_config['parser_module']}: {e}")
        except Exception as e:
            print(f"Error parsing {actor_name}: {e}")
    today = today_date_string()
    output_filename = f"data/event_scraper_output_{today}.xlsx"
    create_sheet(xlsx_rows, output_filename)
    print("Finished. The result can be found in the data directory.")
