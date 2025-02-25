from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os 
app = Flask(__name__)

# Firebase Setup
cred = credentials.Certificate("tethproweb-firebase-adminsdk-a2a9n-1a3a5f1337.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tethproweb-default-rtdb.europe-west1.firebasedatabase.app/'
})

def delete_all_logs_by_id(person_id):
    # Get all logs from the root (or adjust the path if your logs are deeply nested)
    logs_ref = db.reference("/logs")
    
    # Retrieve all the logs
    logs = logs_ref.get()

    # Check if logs exist
    if not logs:
        print("No logs found.")
        return
    
    # Iterate over all names and their logs
    for name, logs_data in logs.items():
        for log_key, log_data in logs_data.items():
            if log_data['id'] == person_id:
                # Delete the log entry
                logs_ref.child(name).child(log_key).delete()
                print(f"Deleted log with ID {person_id} for {name}")
    
    print(f"Finished deleting logs with ID {person_id}.")

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
@app.route('/names')
def get_names():
    names = ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5", "Name 6", "Name 7", "Name 8", "Name 9", "Name 10",
             "Name 11", "Name 12", "Name 13", "Name 14", "Name 15", "Name 16"]
    return jsonify(names)
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

# Route to renjjjjder record page for a specific name
@app.route('/record_page/<name>')
def record_page(name):
    return render_template('record_page.html', name=name)

@app.route('/live-data')
def live_data():
    ref = db.reference('logs')
    data = ref.get()

    today_date = datetime.today().strftime('%Y-%m-%d')
    filtered_data = []

    if data:
        for key, value in data.items():
            for sub_key, sub_value in value.items():
                if sub_value.get('date') == today_date:
                    id_value = sub_value.get('id', 0)
                    if 101 <= id_value <= 116:  # Map IDs to teeth numbers
                        tooth_number = id_value - 100  # Convert 101->1, 102->2, etc.
                        color = 'blue'
                        filtered_data.append({'id': tooth_number, 'color': color})
                    elif 1 <= id_value <= 16:  # IDs directly represent teeth numbers
                        color = 'red'
                        filtered_data.append({'id': id_value, 'color': color})
    return jsonify({'data': filtered_data})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
