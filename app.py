from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for records (you can replace this with a database later)
records = {
    "Name 1": [],
    "Name 2": [],
    "Name 3": []
}

@app.route('/')
def index():
    return "Welcome to the Teth Children Records API!"

@app.route('/names')
def get_names():
    # Return the names available
    names = list(records.keys())
    return jsonify(names)

@app.route('/add_record', methods=['POST'])
def add_record():
    try:
        # Get the data sent from the Raspberry Pi (in JSON format)
        data = request.json  # The data sent from the Raspberry Pi
        
        # Check if all required fields are present
        if not data or 'name' not in data or 'time' not in data or 'id' not in data:
            return jsonify({"message": "Missing required fields."}), 400  # Bad request

        name = data.get('name')
        time = data.get('time')
        person_id = data.get('id')
        date = datetime.now().strftime("%Y-%m-%d")  # Use the current date
        
        # Check if the name exists in records
        if name in records:
            records[name].append({
                'time': time,
                'id': person_id,
                'date': date
            })
            print(f"Updated records for {name}: {records[name]}")  # Debugging line
            return jsonify({"message": "Record added successfully!"}), 200
        else:
            return jsonify({"message": "Name not found!"}), 404

    except Exception as e:
        # If an error occurs, return a 500 error with the exception message
        return jsonify({"message": "Server error", "error": str(e)}), 500


@app.route('/records/<name>', methods=['GET'])
def get_records(name):
    # Get the records for a specific name
    if name in records:
        print(f"Returning records for {name}: {records[name]}")  # Debugging line
        return jsonify(records[name])
    else:
        return jsonify({"message": "Name not found!"}), 404


if __name__ == '__main__':
    app.run(debug=True)
