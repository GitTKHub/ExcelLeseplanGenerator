# Bibliothek importieren
import flet as ft
import pandas as pd
import os
from datetime import datetime

def main(page: ft.Page):
    # Dialogtitel
    page.title = "Leseplan Generator"
#   page.vertical_alignment = ft.MainAxisAlignment.START  

    # Eingabefeld für die Anzahl der Personen und Seitenanzahl für beide Bücher
    person_count_input = ft.TextField(label="Anzahl der Personen", autofocus=True)  # Focus hier
    buch1_pages_input = ft.TextField(label="Seitenanzahl Buch 1", value="")
    buch2_pages_input = ft.TextField(label="Seitenanzahl Buch 2", value="")
    
    # Row für die Eingabefelder erstellen
    input_row = ft.Row(controls=[person_count_input, buch1_pages_input, buch2_pages_input])
    
    person_page_inputs = []  # Liste für die Seitenanzahl jeder Person für beide Bücher
    result_column = ft.Column()

    def create_person_page_inputs():

        # Eingabefelder für die Anzahl der Personen erstellen
        person_count = int(person_count_input.value)

        for i in range(person_count):
            # Eingabefelder für die Seitenanzahl und Startseite in beiden Büchern in einer Zeile
            start_page_buch1_input = ft.TextField(label=f"Person {i+1} - Startseite Buch 1", value="")
            buch1_input = ft.TextField(label=f"Person {i+1} - Seitenanzahl Buch 1", value="5")  # Standard 5
            start_page_buch2_input = ft.TextField(label=f"Person {i+1} - Startseite Buch 2", value="")
            buch2_input = ft.TextField(label=f"Person {i+1} - Seitenanzahl Buch 2", value="5")  # Standard 5
            row = ft.Row(controls=[start_page_buch1_input, buch1_input, start_page_buch2_input, buch2_input])  # Eingabefelder in einer Zeile
            person_page_inputs.append((start_page_buch1_input, buch1_input, start_page_buch2_input, buch2_input))
            page.add(row)  # Zeile zur Seite hinzufügen

        # Excel-Button hinzufügen
        page.add(
            ft.ElevatedButton(text="Leseplan generieren", on_click=generate_plan),
            result_column
        )

        page.update()

    def generate_plan(e):
        # Eingabewerte abrufen
        person_count = int(person_count_input.value)
        buch1_pages = int(buch1_pages_input.value) if buch1_pages_input.value else 0
        buch2_pages = int(buch2_pages_input.value) if buch2_pages_input.value else 0

        # Leseplan erstellen
        leseplan = []
        current_page_buch1 = 1  # Aktuelle Seite für Buch 1
        current_page_buch2 = 1  # Aktuelle Seite für Buch 2

        for idx, person in enumerate([f"Person {i+1}" for i in range(person_count)]):
            # Seitenanzahl für Buch 1 und Buch 2 abrufen
            start_page_buch1 = int(person_page_inputs[idx][0].value) if person_page_inputs[idx][0].value else current_page_buch1
            buch1_pages_per_person = int(person_page_inputs[idx][1].value)
            start_page_buch2 = int(person_page_inputs[idx][2].value) if person_page_inputs[idx][2].value else current_page_buch2
            buch2_pages_per_person = int(person_page_inputs[idx][3].value)

            # Buch 1 Seiten zuweisen
            if start_page_buch1 <= buch1_pages and buch1_pages_per_person > 0:
                buch1_start = start_page_buch1
                buch1_end = min(start_page_buch1 + buch1_pages_per_person - 1, buch1_pages)
                current_page_buch1 = buch1_end + 1  # Nächster Seitenanfang
            else:
                buch1_start = buch1_end = "0"  # 0 schreiben

            # Buch 2 Seiten zuweisen
            if start_page_buch2 <= buch2_pages and buch2_pages_per_person > 0:
                buch2_start = start_page_buch2
                buch2_end = min(start_page_buch2 + buch2_pages_per_person - 1, buch2_pages)
                current_page_buch2 = buch2_end + 1  # Nächster Seitenanfang
            else:
                buch2_start = buch2_end = "0"  # 0 schreiben

            # Leseplan für die Person hinzufügen
            leseplan.append({
                "Person": person,
                "Buch 1 Seiten": f"{buch1_start}-{buch1_end}" if buch1_start != "0" else "0",  # 0 schreiben
                "Buch 2 Seiten": f"{buch2_start}-{buch2_end}" if buch2_start != "0" else "0"   # 0 schreiben
            })

        # DataFrame erstellen
        df = pd.DataFrame(leseplan)

        # Excel-Datei erstellen
        today = datetime.now().strftime("%Y-%m-%d")
        excel_datei = f"Leseplan_{today}.xlsx"
        df.to_excel(excel_datei, index=False)

        # Erfolgsnachricht anzeigen
        result_column.controls.append(ft.Text(f"Leseplan wurde erfolgreich für den {today} erstellt!"))
        page.update()
        
        # Excel-Datei öffnen
        os.startfile(excel_datei)

    # Anzahl der Personen ändern, um die Eingabefelder zu erstellen
    person_count_input.on_change = lambda e: create_person_page_inputs()

    # Fügen Sie die Eingabefelder zur Seite hinzu
    page.add(input_row)  # Eingabefelder in einer Zeile hinzufügen

# Flet-Anwendung starten und main-Funktion als Ziel festlegen
ft.app(target=main)