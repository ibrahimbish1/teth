from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory data store for demo purposes (you can replace it with a database)
names = ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6"]
records = {
    "Name 1": [
        {"time": "10:00", "id": "A123", "date": "2024-11-05"},
        {"time": "12:00", "id": "A124", "date": "2024-11-05"}
    ],
    "Name 2": [
        {"time": "09:00", "id": "B123", "date": "2024-11-05"}
    ],
    # Add more names and records as needed
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/names')
def get_names():
    """
    Returns a list of names (for the home page).
    """
    return jsonify(names)

@app.route('/records/<name>')
def get_records(name):
    """
    Returns the records for a specific name.
    """
    if name in records:
        sorted_records = sorted(records[name], key=lambda x: x['date'])
        records_by_date = {}
        for record in sorted_records:
            date = record['date']
            if date not in records_by_date:
                records_by_date[date] = []
            records_by_date[date].append(record)
        return jsonify(records_by_date)
    else:
        return jsonify({"message": "No records found for this name."})

@app.route('/record_page/<name>')
def record_page(name):
    """
    Renders the record page for a specific name.
    """
    return render_template('record_page.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
