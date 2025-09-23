# 2B-BIM Hackathon

Dieses Projekt stellt eine kleine Webanwendung bereit, um **AIA-Daten (Auftraggeber-Informationsanforderungen)** zu generieren.  
Die Anwendung kombiniert ein Flask-Backend mit einem einfachen Frontend (HTML/JS).

---

## ⚙️ Funktionen

- **Kriterien-Auswahl**: Nutzer können Kriterien über eine Checkliste auswählen und optional Werte eingeben.  
- **Datei-Upload**: `.ids`-Dateien können direkt hochgeladen werden.  
- **Alternativ**: Statt einer Datei kann eine **GUID** angegeben werden, die eine `.ids`-Datei über das BIM-Deutschland-API (`via.bund.de`) lädt.  
- **Mapping**: Kriterien werden über eine JSON-Mappingdatei in Merkmale übersetzt.  
- **Speicherung**: Dateien werden lokal im Ordner `uploads/` abgelegt.  
- **Antwort**: Das Backend gibt die gemappten Merkmale als JSON zurück.  

---

## 📂 Projektstruktur

```

.
├── app.py              # Flask-Backend (Routen und Logik)
├── templates/
│   ├── base.html       # Base Skeleton
│   ├── index.html      # Startseite mit Formular
│   └── animation.html  # Beispielseite für GET /submit
├── static/
│   └── js/
│       └── main.js     # Frontend-Logik (Formular, API-Aufruf)
├── criteria.json       # Kriterienliste
├── mapping.json        # Mapping von Kriterien zu Merkmale
└── uploads/            # Ordner für hochgeladene .ids-Dateien

````

---

## 🚀 Installation & Start

### 1. Repository klonen
```bash
git clone https://github.com/ninakraut/hackathon2025.git
cd hackathon2025
````

### 2. Virtuelle Umgebung erstellen & aktivieren

```bash
pip install uv
```

### 3. Abhängigkeiten installieren

```bash
uv sync
```

### 4. Anwendung starten

```bash
flask --app main.py run
```

Standardmäßig läuft die Anwendung unter:
👉 `http://127.0.0.1:5000`

---

## 📝 Verwendung

1. Startseite (`/`) öffnen.
2. Projektnamen und Beschreibung eingeben.
3. Kriterien auswählen und ggf. Werte hinzufügen.
4. Entweder:

   * `.ids`-Datei hochladen
   * **oder** GUID eintragen (dann wird die Datei automatisch geladen)
5. Klick auf **"AIA Generieren"** → Daten werden an das Backend gesendet.
6. Ergebnis: Liste gemappter Merkmale (JSON).

---

## ⚠️ Hinweise

* Die hochgeladenen Dateien werden im Ordner `uploads/` gespeichert.
* Nur Dateien mit der Endung `.ids` sind erlaubt.

---

## 📌 ToDo

* [ ] Validierung der Formulareingaben erweitern