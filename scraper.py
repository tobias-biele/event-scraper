import importlib
from actors import actors

for actor_name, actor_config in actors.items():
    try:
        parser_module = importlib.import_module(actor_config["parser_module"])
        parse = parser_module.parse
        events = parse(actor_config["url"])

        # Process the parsed data as needed
        # For example, you can save it to a database or file.
        print(f"Actor: {actor_name}")
        print(events)

    except ImportError as e:
        print(f"Error importing {actor_config['parser_module']}: {e}")