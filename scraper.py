import importlib
from actors import actors
from excel import create_sheet

def run(parse_details_pages=False, filter=None):
    options = {
        "parse_details_pages": parse_details_pages,
    }
    print("Starting...")
    if options["parse_details_pages"]:
        print("The scraper will parse details pages. This might take a while.")
    else:
        print("The scraper will not parse details pages.")

    xlsx_rows = []
    for actor_name, actor_config in actors.items():
        try:
            parser_module = importlib.import_module(actor_config["parser_module"])
            parse = parser_module.parse
            events = parse(actor_config["url"], options)
            print("Scraped", len(events), "events from", actor_name)
            xlsx_rows.extend([event.to_xlsx_row() for event in events if filter(event)])
        except ImportError as e:
            print(f"Error importing {actor_config['parser_module']}: {e}")
    create_sheet(xlsx_rows)
