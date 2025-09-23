from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def feedback():
    with open('criteria.json', 'r') as file:
        criteria = json.load(file)
    
    output = []
    for c in criteria:
        output.append(f"Das Kriterium {c} wurde ergänzt.")

    return output