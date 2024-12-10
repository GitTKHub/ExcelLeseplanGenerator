# Excel Reading Plan Generator Documentation

## Overview  
This code generates a reading plan based on the number of participants and the page numbers of two books. It allows users to customize start pages and the number of pages for each individual. The reading plan is exported as an Excel file and automatically opened.

---

## Requirements  
- **Libraries**:  
  - `flet`: For building the GUI
  - `pandas`: For data processing and Excel export  
  - `os`: For opening files
  - `datetime`: For opening files
- **Python-Version**: Python 3.7 or higher  

---

## Code Structure  

### **1. Importing Libraries**
```python
import flet as ft
import pandas as pd
import os
from datetime import datetime
```
- All required libraries are imported.

---

### **2. Main Function: `main`**  
The `main` function serves as the entry point of the application. It is called by the Flet framework.

```python
def main(page: ft.Page):
    page.title = "Leseplan Generator"
```
- **`page`**: Represents the main window of the app  
- **`page.title`**: Sets the title of the application

---

### **3. Input Fields for Participants and Page Numbers**  
The first row contains three input fields:  
- Number of participants  
- Total pages for Book 1
- Total pages for Book 2

```python
person_count_input = ft.TextField(label="Anzahl der Personen", autofocus=True)
buch1_pages_input = ft.TextField(label="Seitenanzahl Buch 1", value="")
buch2_pages_input = ft.TextField(label="Seitenanzahl Buch 2", value="")
input_row = ft.Row(controls=[person_count_input, buch1_pages_input, buch2_pages_input])
```

---

### **4. Dynamic Input Field Generation**  
Based on the number of participants, input fields for each individual are dynamically generated.

```python
def create_person_page_inputs():
    person_count = int(person_count_input.value)
    for i in range(person_count):
        start_page_buch1_input = ft.TextField(label=f"Person {i+1} - Startseite Buch 1", value="")
        buch1_input = ft.TextField(label=f"Person {i+1} - Seitenanzahl Buch 1", value="5")
        start_page_buch2_input = ft.TextField(label=f"Person {i+1} - Startseite Buch 2", value="")
        buch2_input = ft.TextField(label=f"Person {i+1} - Seitenanzahl Buch 2", value="5")
        row = ft.Row(controls=[start_page_buch1_input, buch1_input, start_page_buch2_input, buch2_input])
        person_page_inputs.append((start_page_buch1_input, buch1_input, start_page_buch2_input, buch2_input))
        page.add(row)
```

- **Input Fields per Participant:**:  
  - **Start Page Book 1**  
  - **Pages Book 1**  
  - **Start Page Book 2**  
  - **Pages Book 2**

---

### **5. Generating the Reading Plan**  
The function creates the reading plan based on user inputs and exports it as an Excel file.

```python
def generate_plan(e):
    person_count = int(person_count_input.value)
    buch1_pages = int(buch1_pages_input.value) if buch1_pages_input.value else 0
    buch2_pages = int(buch2_pages_input.value) if buch2_pages_input.value else 0

    leseplan = []
    current_page_buch1 = 1
    current_page_buch2 = 1

    for idx, person in enumerate([f"Person {i+1}" for i in range(person_count)]):
        start_page_buch1 = int(person_page_inputs[idx][0].value) if person_page_inputs[idx][0].value else current_page_buch1
        buch1_pages_per_person = int(person_page_inputs[idx][1].value)
        start_page_buch2 = int(person_page_inputs[idx][2].value) if person_page_inputs[idx][2].value else current_page_buch2
        buch2_pages_per_person = int(person_page_inputs[idx][3].value)

        if start_page_buch1 <= buch1_pages:
            buch1_start = start_page_buch1
            buch1_end = min(start_page_buch1 + buch1_pages_per_person - 1, buch1_pages)
            current_page_buch1 = buch1_end + 1
        else:
            buch1_start = buch1_end = "0"

        if start_page_buch2 <= buch2_pages:
            buch2_start = start_page_buch2
            buch2_end = min(start_page_buch2 + buch2_pages_per_person - 1, buch2_pages)
            current_page_buch2 = buch2_end + 1
        else:
            buch2_start = buch2_end = "0"

        leseplan.append({
            "Person": person,
            "Buch 1 Seiten": f"{buch1_start}-{buch1_end}" if buch1_start != "0" else "0",
            "Buch 2 Seiten": f"{buch2_start}-{buch2_end}" if buch2_start != "0" else "0"
        })

    df = pd.DataFrame(leseplan)
    today = datetime.now().strftime("%Y-%m-%d")
    excel_datei = f"Leseplan_{today}.xlsx"
    df.to_excel(excel_datei, index=False)
    os.startfile(excel_datei)
```

---

### **6. Excel Export**
- Saves the reading plan as an Excel file with a date in the file name
- Automatically opens the file using `os.startfile`.

---

### **7. Starting the App**  
At the end, the `main`function is started through the Flet framework  

```python
ft.app(target=main)
```

---

## Improvements  
- **Error Handling**: Handle invalid or negative inputs 
- **UI Optimization**: Organize input fields into panels for better clarity 
- **Data Validation**: Ensure that start pages and page numbers are within valid ranges

