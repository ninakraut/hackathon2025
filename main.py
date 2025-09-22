from flask import Flask
from flask import request
from werkzeug.utils import secure_filename
from flask.templating import render_template
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
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

        # Check if the file was sent and has a filename
        if ids_file and ids_file.filename:
            # Secure the filename to prevent security issues
            filename = secure_filename(ids_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save the file to the configured upload folder
            ids_file.save(filepath)
            print(f"File saved to: {filepath}")
        else:
            # Handle case where no file was uploaded
            filename = "No file uploaded"
            print("No file was uploaded.")

        return mapped_features