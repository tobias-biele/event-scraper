from excel import read_sheet, create_sheet
import os

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

def filter_by_keywords(filename, keywords):
    if not filename.endswith(".xlsx"):
        print("Input must be an Excel file (.xlsx")
    else:
        filename = filename[:-5]
    events = read_sheet(f"data/{filename}.xlsx")
    included = []
    excluded = []
    for event in events:
        for keyword in keywords:
            if keyword.lower() in event.title.lower() or keyword.lower() in str(event.description).lower():
                included.append(event.to_xlsx_row())
                break
        excluded.append(event.to_xlsx_row())
    create_sheet(included, f"data/{filename}_filtered.xlsx")
    create_sheet(excluded, f"data/{filename}_filtered_excluded.xlsx")

files = os.listdir("data")
for file in files:
    if file.endswith(".xlsx") and not file.endswith("_filtered.xlsx") and not file.endswith("_filtered_excluded.xlsx"):
        print(f"Filtering file {file}")
        filter_by_keywords(file, KEYWORDS)