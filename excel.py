import os
import pandas as pd
from event import Event

def create_sheet(data, filename):
    columns = [
        "Von", "Bis", "Uhrzeit", "Titel der Veranstaltung", "Thema",
        "Veranstaltende Institution/Organisation", "Ort", "Zielgruppe", "Link zur VA", "Eintragsdatum", "Detailseite Text"
    ]
    df = pd.DataFrame(data, columns=columns)
    df['date_column'] = pd.to_datetime(df['Von'], format='%d.%m.%Y %H:%M', errors='coerce').combine_first(pd.to_datetime(df['Von'], format='%d.%m.%Y', errors='coerce'))
    df.sort_values(by='date_column', inplace=True)
    df.drop(columns=['date_column'], inplace=True)
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")
    excel_writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="Veranstaltungen", index=False)
    excel_writer._save()

def read_sheet(filename):
    try:
        df = pd.read_excel(filename, sheet_name="Veranstaltungen")
        event_list = []

        for _, row in df.iterrows():
            # Extract the data from the DataFrame
            start = row["Von"]
            end = row["Bis"]
            timeframe = row["Uhrzeit"]
            title = row["Titel der Veranstaltung"]
            topic = row["Thema"]
            actor = row["Veranstaltende Institution/Organisation"]
            target_group = row["Zielgruppe"]
            link = row["Link zur VA"]
            added = row["Eintragsdatum"]
            description = row["Detailseite Text"]

            # Create an Event object and add it to the list
            event = Event(
                title=title,
                start=start,
                end=end,
                timeframe=timeframe,
                topic=topic,
                actor=actor,
                target_group=target_group,
                link=link,
                added=added,
                description=description
            )
            event_list.append(event)

        return event_list
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []
