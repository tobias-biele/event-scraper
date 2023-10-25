import importlib
from actors import actors
from excel import create_sheet

options = {
    "parse_details_pages": False,
}

xlsx_rows = []
for actor_name, actor_config in actors.items():
    try:
        parser_module = importlib.import_module(actor_config["parser_module"])
        parse = parser_module.parse
        events = parse(actor_config["url"], options)
        print("Scrape", len(events), "events from", actor_name)
        xlsx_rows.extend([event.to_xlsx_row() for event in events])
    except ImportError as e:
        print(f"Error importing {actor_config['parser_module']}: {e}")
create_sheet(xlsx_rows)