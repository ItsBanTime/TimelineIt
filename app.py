# Save this as app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from dateutil import parser
import spacy
from datetime import datetime

# Install required packages
# pip install Flask flask_cors spacy python-dateutil

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

nlp = spacy.load("en_core_web_sm")

# Function to extract dates and descriptions
def extract_dates_and_descriptions(text):
    doc = nlp(text)
    events = []
    date_pattern = r'\b(\w+\s+\d{1,2},\s+\d{4}|\d{4})\b'

    for sent in doc.sents:
        match = re.search(date_pattern, sent.text)
        if match:
            try:
                date = parser.parse(match.group(0))
                description = sent.text.strip()
                events.append({"date": date.strftime('%b %d, %Y'), "description": description})
            except ValueError:
                continue
    
    return sorted(events, key=lambda x: datetime.strptime(x['date'], '%b %d, %Y'))

# Flask route to process text input
@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify([])
    
    events = extract_dates_and_descriptions(text)
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
