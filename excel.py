import pandas as pd

def create_sheet(data):
    columns = [
        "Von", "Bis", "Uhrzeit", "Titel der Veranstaltung", "Thema",
        "Veranstaltende Institution/Organisation", "Zielgruppe", "Link zur VA", "Eintragsdatum"
    ]
    df = pd.DataFrame(data, columns=columns)
    excel_writer = pd.ExcelWriter("data/events.xlsx", engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="Veranstaltungen", index=False)
    excel_writer._save()