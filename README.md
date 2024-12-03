# 📚 Excel Leseplan Generator Dokumentation

## Überblick  
Dieser Code generiert einen Leseplan basierend auf der Anzahl der Personen und den Seitenzahlen von zwei Büchern. Es ermöglicht den Benutzern, Startseiten und die Anzahl der Seiten individuell für jede Person festzulegen. Der Leseplan wird als Excel-Datei exportiert und automatisch geöffnet.  

---

## 🛠 Anforderungen  
- **Bibliotheken**:  
  - `flet`: Für die GUI-Erstellung.  
  - `pandas`: Zur Datenverarbeitung und Excel-Export.  
  - `os`: Um Dateien zu öffnen.  
  - `datetime`: Zur Erstellung eines datierten Dateinamens.  
- **Python-Version**: Python 3.7 oder höher.  

---

## 📝 Code-Struktur  

### **1. Bibliotheken Importieren**
```python
import flet as ft
import pandas as pd
import os
from datetime import datetime
```
- Importiert alle erforderlichen Bibliotheken.

---

### **2. Hauptfunktion: `main`**  
Die Funktion `main` ist der Einstiegspunkt der Anwendung. Sie wird vom Flet-Framework aufgerufen.

```python
def main(page: ft.Page):
    page.title = "Leseplan Generator"
```
- **`page`**: Repräsentiert das Hauptfenster der App.  
- **`page.title`**: Setzt den Titel der Anwendung.  

---

### **3. Eingabefelder für Personen und Seitenzahlen**  
Die erste Zeile enthält drei Eingabefelder:  
- Anzahl der Personen.  
- Seitenanzahl für Buch 1.  
- Seitenanzahl für Buch 2.  

```python
person_count_input = ft.TextField(label="Anzahl der Personen", autofocus=True)
buch1_pages_input = ft.TextField(label="Seitenanzahl Buch 1", value="")
buch2_pages_input = ft.TextField(label="Seitenanzahl Buch 2", value="")
input_row = ft.Row(controls=[person_count_input, buch1_pages_input, buch2_pages_input])
```

---

### **4. Dynamische Eingabefelder Generieren**  
Basierend auf der Anzahl der Personen werden Eingabefelder für jede Person dynamisch erstellt.  

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

- **Eingabefelder pro Person**:  
  - **Startseite Buch 1**  
  - **Seitenanzahl Buch 1**  
  - **Startseite Buch 2**  
  - **Seitenanzahl Buch 2**

---

### **5. Leseplan Generieren**  
Die Funktion erstellt den Leseplan basierend auf den Eingaben und exportiert ihn als Excel-Datei.  

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

### **6. Excel-Export**
- Speichert den Leseplan in einer Excel-Datei mit Datum im Dateinamen.  
- Öffnet die Datei automatisch mit `os.startfile`.

---

### **7. App Starten**  
Am Ende wird die `main`-Funktion durch das Flet-Framework gestartet.  

```python
ft.app(target=main)
```

---

## 🚀 Verbesserungsmöglichkeiten  
- **Fehlerbehandlung**: Negative oder nicht-numerische Eingaben abfangen.  
- **UI-Optimierung**: Eingabefelder in Panels organisieren.  
- **Datenvalidierung**: Prüfen, ob die Startseite und Seitenanzahl innerhalb gültiger Grenzen liegen.  

