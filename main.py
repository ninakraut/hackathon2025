from flask import Flask
from flask import request
from werkzeug.utils import secure_filename
from flask.templating import render_template
import json
import os
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
if(not os.path.exists(app.config["UPLOAD_FOLDER"])):
    os.mkdir(app.config["UPLOAD_FOLDER"])

@app.route("/")
def main():
    criteria = json.load(open("criteria.json"))

    return render_template("index.html", data=criteria)

def map_criteria_to_features(criteria_list, mapping):
    all_features = []

    for criterion in criteria_list:
        group = criterion["group"]
        name = criterion["criterion"]
        if group in mapping and name in mapping[group]:
            features = mapping[group][name]
            all_features.extend(features)
    
    # Entfernen von Duplikaten und Sortieren der Merkmale
    unique_features = sorted(list(set(all_features)))
    
    return unique_features

ALLOWED_EXTENSIONS = {'ids'}
@app.route("/submit", methods=["get", "post"])
def submit():
    if request.method == "GET":
        return render_template("animation.html")
    else:
        data = request.form
        if not data or "criteria" not in data:
            return {"error": "Invalid request data"}, 400
        
        criteria_list = json.loads(data.get("criteria", "[]"))
        mapping_data = json.load(open("mapping.json"))

        mapped_features = map_criteria_to_features(criteria_list, mapping_data)

        # Access uploaded files via request.files
        ids_file = request.files.get('idsFile')
        ids_guid = data.get('idsGUID', "")

        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        # check if file was selected
        if not ids_file or ids_file.filename == '':
            if ids_guid:
                response = requests.get(f"https://via.bund.de/bim/aia/api/v1/public/aiaProject/{ids_guid}/IDS")
                if response.status_code == 200:
                    with open(app.config["UPLOAD_FOLDER"] + "/test.ids", "w") as fp:
                        fp.write(response.text)
                else:
                    print(f"Error getting IDS: {response.status_code}\n{response.text}")
            else:
                return {'error': 'No file selected'}, 400
        else:
            # check if file has .ids extension
            if not allowed_file(ids_file.filename):
                return {'error': 'Only .ids files are allowed'}, 400

            # Secure the filename to prevent security issues
            filename = secure_filename(ids_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save the file to the configured upload folder
            ids_file.save(filepath)
            print(f"File saved to: {filepath}")

        return mapped_features