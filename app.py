from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Firebase Setup
cred = credentials.Certificate(r"tethproweb-firebase-adminsdk-a2a9n-1a3a5f1337.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tethproweb-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Route to render the main page (changed to index.html)
@app.route('/')
def ind():
    return render_template('ind.html')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/live')
def live():
    today_date = datetime.today().strftime('%Y-%m-%d')
    return render_template('live.html', today_date=today_date)

# Route to provide live data
@app.route('/live-data')
def live_data():
    ref = db.reference('logs')  # Reference to Firebase 'logs' node
    data = ref.get()  # Get data from Firebase

    today_date = datetime.today().strftime('%Y-%m-%d')
    filtered_data = []

    if data:
        for key, value in data.items():  # Loop over each "Name" node
            for sub_key, sub_value in value.items():  # Loop over each log under "Name"
                if sub_value.get('date') == today_date and (1 <= sub_value.get('id', 0) <= 16):
                    id_str = str(sub_value.get('id'))
                    color = 'white' if '9' in id_str else 'red'
                    filtered_data.append({'id': sub_value.get('id'), 'color': color})

    return jsonify({'data': filtered_data})  # Return filtered data as JSON

# Route to get the list of names (from Firebase or static list)
@app.route('/names')
def get_names():
    names = ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6", "Name 7", "Name 8", "Name 9", "Name 10",
             "Name 11", "Name 12", "Name 13", "Name 14", "Name 15", "Name 16"]
    return jsonify(names)

# Route to get records for a specific name
@app.route('/records/<name>')
def get_records(name):
    records_ref = db.reference(f"/logs/{name}")
    records = records_ref.get()

    if records:
        # Organize records by date
        sorted_records = sorted(records.values(), key=lambda x: x.get('date', ''))
        records_by_date = {}
        for record in sorted_records:
            date = record.get('date', 'N/A')
            records_by_date.setdefault(date, []).append(record)
        return jsonify(records_by_date)
    else:
        return jsonify({"message": "No records found."})

# Route to render record page for a specific name
@app.route('/record_page/<name>')
def record_page(name):
    return render_template('record_page.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, jsonify
# from firebase_admin import credentials, initialize_app, db

# app = Flask(__name__)

# # Firebase Setup
# cred = credentials.Certificate("tethproweb-firebase-adminsdk-a2a9n-1a3a5f1337.json")
# initialize_app(cred, {
#     'databaseURL': 'https://tethproweb-default-rtdb.europe-west1.firebasedatabase.app/'
# })

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/names')
# def get_names():
#     # You can load names from Firebase ifmmmm needed
#     names = ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6", "Name 7", "Name 8", "Name 9", "Name 10",
#              "Name 11", "Name 12", "Name 13", "Name 14", "Name 15", "Name 16"]
#     return jsonify(names)

# @app.route('/records/<name>')
# def get_records(name):
#     records_ref = db.reference(f"/logs/{name}")
#     records = records_ref.get()

#     if records:
#         # Organize records by date
#         sorted_records = sorted(records.values(), key=lambda x: x.get('date', ''))
#         records_by_date = {}
#         for record in sorted_records:
#             date = record.get('date', 'N/A')
#             records_by_date.setdefault(date, []).append(record)
#         return jsonify(records_by_date)
#     else:
#         return jsonify({"message": "No records found."})

# @app.route('/record_page/<name>')
# def record_page(name):
#     return render_template('record_page.html', name=name)

# if __name__ == '__main__':
#     app.run(debug=True)
