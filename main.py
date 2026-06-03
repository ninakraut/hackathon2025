from bs4 import BeautifulSoup, Tag
from flask import Flask
from flask import request
from werkzeug.utils import secure_filename
from flask.templating import render_template
from pathlib import Path
import json
import os
import requests

import aia

# Flask-App initialisieren
app = Flask(__name__)
# Upload-Verzeichnis konfigurieren
app.config['UPLOAD_FOLDER'] = "uploads"
# Falls der Upload-Ordner nicht existiert, wird er erstellt
if(not os.path.exists(app.config["UPLOAD_FOLDER"])):
    os.mkdir(app.config["UPLOAD_FOLDER"])

# Route für die Startseite
@app.route("/")
def main():
    # Kriterien aus XML-Datei laden
    catalogs = load_criteria_catalogs()
    criteria = []
    if catalogs:
        for soup in catalogs:
            # Map of propertyGroup guid to propertyGroup info
            groups = {}
            for group in soup.find_all("propertyGroup"):
                guid_el = group.find("guid")
                names_el = group.find("namesInLanguage")
                if guid_el and names_el:
                    name_el = names_el.find("name")
                    if name_el:
                        groups[guid_el.text.strip()] = {
                            "name": name_el.text.strip(),
                            "properties": []
                        }

            # Map of properties to groups
            for prop in soup.find_all("property"):
                names_el = prop.find("namesInLanguage")
                group_guid_el = prop.find("groupOfProperties")
                if names_el and group_guid_el:
                    name_el = names_el.find("name")
                    if name_el:
                        prop_name = name_el.text.strip()
                        group_guid = group_guid_el.text.strip()
                        if group_guid in groups:
                            groups[group_guid]["properties"].append(prop_name)

            criteria.extend(groups.values())

    # Übergabe der Kriterien an das Template "index.html"
    return render_template("index.html", data=criteria)

# Hilfsfunktion: Kriterien in Merkmale abbilden
def map_criteria_to_features(criteria_list: list[str], catalogs: list[BeautifulSoup]) -> list[Tag]:
    u"""Loads XML file containing all criteria and properties and returns a unique set of properties based on user selection.

    Parameters:
        `criteria_list`: List of criteria GUIDs to map
        `catalogs`: Catalog of all criteria and respective property mappings

    Returns:
          `unique_features`: List of unique properties based on user selection`
    """

    unique_properties = set()

    for c in catalogs:
        props = c.find_all('property')
        unique_properties = unique_properties.union(props)

    # Add all unselected properties to set and use difference for removal
    unselected_properties = set()
    for p in unique_properties:
        guid = p.groupOfProperties.get_text()
        if guid not in criteria_list:
            unselected_properties.add(p)

    print(f"Selected {len(criteria_list)} criteria")
    print(f"Mapped selected criteria to {len(unique_properties) - len(unselected_properties)} out of {len(unique_properties)} unique properties")

    unique_properties.difference_update(unselected_properties)

    return list(unique_properties)


def load_criteria_catalogs() -> list[BeautifulSoup]:
    u"""Loads XML file containing all criteria and returns list of parsed XML documents."""

    # Add paths to further catalogs here to expand tool
    catalog_paths = ["2026_06_01_RUB_Merkmale_Nachhaltigkeit.xml"]

    catalogs = []
    for c_path in catalog_paths:
        with Path(c_path).resolve().open("r") as fp:
            catalogs.append(BeautifulSoup(fp, "xml"))
    return catalogs


# Erlaubte Dateiendungen für Uploads (hier nur .ids)
ALLOWED_EXTENSIONS = {'ids'}

# Route für Formular-Submit (GET und POST möglich)
@app.route("/submit", methods=["get", "post"])
def submit():
    if request.method == "GET":
        # Bei GET: Template mit Ergebnis laden
        return render_template("result.html")
    else:
        # Bei POST: Formular-Daten verarbeiten
        data = request.form
        if not data or "criteria" not in data:
            return {"error": "Invalid request data"}, 400

        #TODO: Adapt to retrieve criteria GUID from form

        # Kriterien aus Formular auslesen
        criteria_list = json.loads(data.get("criteria", "[]"))

        # Features aus Mapping ableiten
        criteria_catalogs = load_criteria_catalogs()
        mapped_features = map_criteria_to_features(criteria_list, criteria_catalogs)

        # Hochgeladene Datei auslesen
        ids_file = request.files.get('idsFile')
        # Alternativ: GUID (falls keine Datei hochgeladen wurde)
        ids_guid = data.get('idsGUID', "")

        # Hilfsfunktion: prüft, ob Dateiendung erlaubt ist
        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        # Prüfen, ob eine Datei hochgeladen wurde
        if not ids_file or ids_file.filename == '':
            # Falls stattdessen eine GUID übergeben wurde
            if ids_guid:
                # Anfrage an externes API stellen, um IDS-Datei zu laden
                response = requests.get(f"https://via.bund.de/bim/aia/api/v1/public/aiaProject/{ids_guid}/IDS")
                if response.status_code == 200:
                    # Datei lokal speichern
                    with open(app.config["UPLOAD_FOLDER"] + "/test.ids", "w") as fp:
                        fp.write(response.text)
                        filepath = os.path.join(app.config["UPLOAD_FOLDER"], "test.ids")
                else:
                    # Fehlerfall beim API-Request
                    print(f"Error getting IDS: {response.status_code}\n{response.text}")
            else:
                # Weder Datei noch GUID vorhanden → Fehler
                return {'error': 'No file selected'}, 400
        else:
            # Falls Datei hochgeladen: Endung prüfen
            if not allowed_file(ids_file.filename):
                return {'error': 'Only .ids files are allowed'}, 400

            # Dateiname absichern (gegen Directory Traversal etc.)
            filename = secure_filename(ids_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Datei im Upload-Ordner speichern
            ids_file.save(filepath)
            print(f"File saved to: {filepath}")

        enhancer = aia.AiaEnhancer()
        # Read original ids
        with open(filepath, "r") as fp:
            ids_file = fp.read()
        modified_ids = enhancer.check_and_add_properties(ids_file, mapped_features)
        # Ergebnis zurückgeben (Liste der gemappten Features)
        with open(f"static/new.ids", "w") as fp:
            fp.write(modified_ids)

        return {"Response status": "Success"}, 200
