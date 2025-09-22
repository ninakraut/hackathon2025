from flask import Flask
from flask.templating import render_template
import json

app = Flask(__name__)

@app.route("/")
def main():
    criteria = json.load(open("criteria.json"))

    return render_template("index.html", data=criteria)

@app.route("/submit")
def animation():
    return render_template("animation.html")