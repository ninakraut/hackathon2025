# 2B-BIM Hackathon

Dieses Projekt stellt eine Webanwendung bereit, um **AIA-Daten (Auftraggeber-Informationsanforderungen)** auf ausgewählte Nachhaltigkeitskriterien prüfen und die nötigen Merkmale gegebenenfalls zu ergänzen.  
Die Anwendung kombiniert ein Flask-Backend mit einem einfachen Frontend (HTML/JS) und bindet das BIM-Portal per API an.
Autoren/Teammitglieder sind Daniel Gerdes ([NietroMiner00](https://github.com/NietroMiner00)), Rosa Alani ([Azorios](https://github.com/Azorios)), Nina Krautgartner ([ninakraut](https://github.com/ninakraut)), Felix Rosenthal ([FeR0se](https://github.com/FeR0se)), Johannes Reinders

---

## ⚙️ Funktionen

- **Kriterien-Auswahl**: Nutzer können Kriterien über eine Checkliste auswählen und optional Werte eingeben.  
- **Datei-Upload**: `.ids  `-Dateien können direkt hochgeladen oder alternativ mittels **GUID** über das BIM-Deutschland-API (`via.bund.de`) geladen werden.
- **Mapping**: Nachhaltigkeitskriterien werden über eine JSON-Mappingdatei in Merkmale übersetzt.
- **Antwort**: Das Backend exportiert die geprüfte und ggf. erweiterte `.ids`-Datei zum Download.   

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
