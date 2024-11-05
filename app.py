from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for received data (replace with a database like PostgreSQL or SQLite for persistence)
data_store = []

@app.route('/')
def index():
    return "Welcome to the Data Receiver!"

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # Get JSON data from the request
    data = request.json

    # If no data is provided, return an error message
    if not data:
        return jsonify({"message": "No data provided or malformed JSON!"}), 400

    # Append the data to our in-memory store (replace with a real database if needed)
    data_store.append(data)

    print(f"Received data: {data}")  # For debugging purposes

    return jsonify({"message": "Data received successfully!"}), 200

@app.route('/get_data', methods=['GET'])
def get_data():
    # Return all the stored data
    return jsonify({"data": data_store})

if __name__ == '__main__':
    app.run(debug=True)
