from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

critiria = {
  "Gestaltung": [
    "Level of Detail (LOD)",
    "Level of Information Need (LOIN)",
    "Visuelle Qualität"
  ],
  "Nachhaltigkeit": [
    "Energieeffizienz",
    "Cradle-to-Cradle-Prinzip",
    "Lebenszyklusanalyse (LCA)"
  ],
  "Funktionalität": [
    "Benutzerfreundlichkeit",
    "Kompatibilität",
    "Sicherheit"
  ]
}

@app.route("/")
def main():
    return render_template("index.html", data=critiria)

@app.route("/submit")
def animation():
    return render_template("animation.html")