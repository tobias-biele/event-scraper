from excel import read_sheet, create_sheet

# PARAMETER SECTION
# --------------------------------
KEYWORDS = [
        "Hitze", 
        "Starkregen", 
        "Hochwasser", 
        "Trockenheit", 
        "Dürre", 
        "Naturbasiert", 
        "Biodiversität", 
        "Stadtgrün", 
        "Bürgerkommunikation", 
        "Stadtplanung", 
        "Bauleitplanung", 
        "Gesundheit", 
        "Eigenvorsorge", 
        "Verbraucherschutz", 
        "Akteurskommunikation", 
        "Verkehrsplanung",
        "Straßengestaltung",
    ]
# --------------------------------

def filter_by_keywords(keywords):
    events = read_sheet("data/events.xlsx")
    included = []
    excluded = []
    for event in events:
        for keyword in keywords:
            if keyword.lower() in event.title.lower() or keyword.lower() in str(event.description).lower():
                included.append(event.to_xlsx_row())
                break
        excluded.append(event.to_xlsx_row())
    create_sheet(included, "data/events_filtered.xlsx")
    create_sheet(excluded, "data/events_filtered_excluded.xlsx")

filter_by_keywords(KEYWORDS)