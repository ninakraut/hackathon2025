from flask import Flask
from flask import request
from flask.templating import render_template
import json

app = Flask(__name__)

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
        data = request.get_json()
        if not data or "criteria" not in data:
            return {"error": "Invalid request data"}, 400
        
        criteria_list = data.get("criteria", [])
        mapping_data = json.load(open("mapping.json"))

        mapped_features = map_criteria_to_features(criteria_list, mapping_data)

        return mapped_features