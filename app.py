from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulating an in-memory data storage (you can replace this with a database like SQLite or PostgreSQL)
data_store = []

@app.route('/')
def index():
    return "Welcome to the Sensor Data API!"

@app.route('/send_data', methods=['POST'])
def receive_data():
    # Get JSON data from the request
    data = request.json

    # Check if data is provided
    if not data:
        return jsonify({"message": "No data provided or malformed JSON!"}), 400

    # Store the received data (in-memory storage, replace with a database if needed)
    data_store.append(data)

    print(f"Received data: {data}")  # For debugging, print the received data

    return jsonify({"message": "Data received successfully!"}), 200

@app.route('/get_data', methods=['GET'])
def send_data():
    # Return all stored data
    return jsonify({"data": data_store})

if __name__ == '__main__':
    app.run(debug=True)
