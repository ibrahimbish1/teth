from flask import Flask, render_template, jsonify, request, redirect, url_for
from firebase_admin import credentials, initialize_app, db
from datetime import datetime

app = Flask(__name__)

# Firebase Setup
cred = credentials.Certificate(r"teth-d96f6-firebase-adminsdk-d8p84a10768.json")
initialize_app(cred, {
    'databaseURL': 'https://teth-d96f6-default-rtdb.eurFDFDoFpe-west1.firebasedatabase.app/'
})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/names')
def get_names():
    # You can change this to fetch names from Firebase if needed
    names = [
        "Name 1", "Name 2", "Name 3", "Name 4", "Name 5",
        "Name 6", "Name 7", "Name 8", "Name 9", "Name 10",
        "Name 11", "Name 12", "Name 13", "Name 14", "Name 15", "Name 16"
    ]
    return jsonify(names)

@app.route('/records/<name>')
def get_records(name):
    records_ref = db.reference(f"/logs/{name}")
    records = records_ref.get()
    if records:
        sorted_records = sorted(records.values(), key=lambda x: x.get('date', ''))
        records_by_date = {}
        for record in sorted_records:
            date = record.get('date', 'N/A')
            if date not in records_by_date:
                records_by_date[date] = []
            records_by_date[date].append(record)
        return jsonify(records_by_date)
    else:
        return jsonify({"message": "No records found."})

@app.route('/record_page/<name>')
def record_page(name):
    return render_template('record_page.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
