from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory storage (just for example, replace with file/database if needed)
data_store = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_data', methods=['POST'])
def send_data():
    """
    Receives data from Raspberry Pi and stores it in-memory or logs it.
    """
    try:
        data = request.get_json()
        name = data.get('name')
        value = data.get('value')
        
        if not name or not value:
            return jsonify({"error": "Missing 'name' or 'value'"}), 400

        # Store data in memory (you can replace this with a file or database if necessary)
        timestamp = datetime.utcnow().isoformat()
        record = {
            "name": name,
            "value": value,
            "timestamp": timestamp
        }
        data_store.append(record)  # Store in memory for now

        return jsonify({"message": "Data received and stored successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_data')
def get_data():
    """
    Returns the stored data (for example, to view it from a web interface).
    """
    return jsonify(data_store)

if __name__ == '__main__':
    app.run(debug=True)
