# Import library
import flet as ft
import pandas as pd
import os
from datetime import datetime


def main(page: ft.Page):

    # Dialog title
    page.title = "Leseplan Generator"

    # Input fields for number of people and page count for both books
    person_count_input = ft.TextField(label="Anzahl der Personen", autofocus=True)  # Focus here
    buch1_pages_input = ft.TextField(label="Seitenanzahl Buch 1", value="")
    buch2_pages_input = ft.TextField(label="Seitenanzahl Buch 2", value="")
    
    # Create row for input fields
    input_row = ft.Row(controls=[person_count_input, buch1_pages_input, buch2_pages_input])
    
    # List for the page count of each person for both books
    person_page_inputs = []
    
    result_column = ft.Column()

    def create_person_page_inputs():

        person_count = int(person_count_input.value)

        # Create input fields for the number of people
        for i in range(person_count):
            # Input fields for the page count and starting page in both books in a row
            start_page_buch1_input = ft.TextField(label=f"Person {i+1} - Startseite Buch 1", value="")
            # Default 5
            buch1_input =  ft.TextField(label=f"Person {i+1} - Seitenanzahl Buch 1", value="5")

            # Input fields for the page count and starting page in both books in a row
            start_page_buch2_input = ft.TextField(label=f"Person {i+1} - Startseite Buch 2", value="")
            # Default 5
            buch2_input = ft.TextField(label=f"Person {i+1} - Seitenanzahl Buch 2", value="5")

            # Input fields in a row (tuple)
            row = ft.Row(controls=[start_page_buch1_input, buch1_input, start_page_buch2_input, buch2_input])  
            person_page_inputs.append((start_page_buch1_input, buch1_input, start_page_buch2_input, buch2_input))
            # Add row to page
            page.add(row)

        # Add Excel button
        page.add(
            ft.ElevatedButton(text="Leseplan generieren", on_click=generate_plan),
            result_column
        )

        page.update()

    def generate_plan(e):
        # Retrieve input values
        person_count = int(person_count_input.value)
        buch1_pages = int(buch1_pages_input.value) if buch1_pages_input.value else 0
        buch2_pages = int(buch2_pages_input.value) if buch2_pages_input.value else 0

        # Create reading plan
        leseplan = []
        current_page_buch1 = 1  # Aktuelle Seite für Buch 1
        current_page_buch2 = 1  # Aktuelle Seite für Buch 2

        for idx, person in enumerate([f"Person {i+1}" for i in range(person_count)]):
            # Retrieve page count for book 1 and book 2
            start_page_buch1 = int(person_page_inputs[idx][0].value) if person_page_inputs[idx][0].value else current_page_buch1
            buch1_pages_per_person = int(person_page_inputs[idx][1].value)
            start_page_buch2 = int(person_page_inputs[idx][2].value) if person_page_inputs[idx][2].value else current_page_buch2
            buch2_pages_per_person = int(person_page_inputs[idx][3].value)

            # Assign pages for book 1
            if start_page_buch1 <= buch1_pages and buch1_pages_per_person > 0:
                buch1_start = start_page_buch1
                buch1_end = min(start_page_buch1 + buch1_pages_per_person - 1, buch1_pages)
                # Next starting page
                current_page_buch1 = buch1_end + 1
            else:
                # Write 0
                buch1_start = buch1_end = "0"

            # Assign pages for book 2
            if start_page_buch2 <= buch2_pages and buch2_pages_per_person > 0:
                buch2_start = start_page_buch2
                buch2_end = min(start_page_buch2 + buch2_pages_per_person - 1, buch2_pages)
                # Next starting page
                current_page_buch2 = buch2_end + 1 
            else:
                # Write 0
                buch2_start = buch2_end = "0"

            # Assign pages for book 2
            leseplan.append({
                "Person": person,
                "Buch 1 Seiten": f"{buch1_start}-{buch1_end}" if buch1_start != "0" else "0",  # Write 0
                "Buch 2 Seiten": f"{buch2_start}-{buch2_end}" if buch2_start != "0" else "0"   # Write 0
            })

        # Create DataFrame
        df = pd.DataFrame(leseplan)

        # Create Excel file
        today = datetime.now().strftime("%Y-%m-%d")
        excel_datei = f"Leseplan_{today}.xlsx"
        df.to_excel(excel_datei, index=False)

        # Show success message
        result_column.controls.append(ft.Text(f"Leseplan wurde erfolgreich für den {today} erstellt."))
        page.update()
        
        # Open Excel file
        os.startfile(excel_datei)

    # Change number of people to create input fields
    person_count_input.on_change = lambda e: create_person_page_inputs()

    # Add input fields to the page in a row
    page.add(input_row)

# Start Flet application
ft.app(target=main)