from flask import Flask
from flask import request
from werkzeug.utils import secure_filename
from flask.templating import render_template
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
    # Kriterien aus JSON-Datei laden
    criteria = json.load(open("criteria.json", encoding="utf8"))

    # Übergabe der Kriterien an das Template "index.html"
    return render_template("index.html", data=criteria)

# Hilfsfunktion: Kriterien in Merkmale abbilden
def map_criteria_to_features(criteria_list, mapping):
    all_features = set()

    # load property information and transform into dataclass
    with open("properties.json") as property_information:
        property_data = json.load(property_information)
    properties = [aia.Property(**prop) for prop in property_data]

    for criterion in criteria_list:
        group = criterion["group"]      # z. B. Kategorie der Kriterien
        name = criterion["criterion"]   # konkretes Kriterium
        # Prüfen, ob Mapping für diese Gruppe und Kriterium existiert
        if group in mapping and name in mapping[group]:
            feature_names = mapping[group][name]
            for feature in feature_names:
                match = next((p for p in properties if p.name == feature), None)
                all_features.add(match)  # Features hinzufügen
    
    # Entfernen von Duplikaten und Sortieren der Merkmale
    unique_features = list(all_features)
    
    return unique_features

# Erlaubte Dateiendungen für Uploads (hier nur .ids)
ALLOWED_EXTENSIONS = {'ids'}

# Route für Formular-Submit (GET und POST möglich)
@app.route("/submit", methods=["get", "post"])
def submit():
    if request.method == "GET":
        # Bei GET: Template mit Animation laden
        return render_template("animation.html")
    else:
        # Bei POST: Formular-Daten verarbeiten
        data = request.form
        if not data or "criteria" not in data:
            return {"error": "Invalid request data"}, 400
        
        # Kriterien aus Formular auslesen
        criteria_list = json.loads(data.get("criteria", "[]"))
        # Mapping aus Datei laden
        mapping_data = json.load(open("mapping.json"))

        # Features aus Mapping ableiten
        mapped_features = map_criteria_to_features(criteria_list, mapping_data)

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
