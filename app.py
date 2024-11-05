import os
import json
from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests  # to send data to/from external sources
from datetime import datetime

app = Flask(__name__)

# The Heroku app's endpoint URL to get/send data (update with your actual Heroku URL)
heroku_url = "https://your-heroku-app-name.herokuapp.com/data"
get_data_url = "https://your-heroku-app-name.herokuapp.com/get-data"

# Route to render index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get names (simulating the retrieval of some data, you could modify as needed)
@app.route('/names')
def get_names():
    # Sample names list for demonstration, can be replaced with any data
    names = ["John", "Jane", "Alice", "Bob", "Charlie", "Eve"]
    return jsonify(names)

# Route to retrieve records (replace with external API fetch)
@app.route('/records/<name>')
def get_records(name):
    # Example: Fetch records from an external source
    response = requests.get(f"{get_data_url}")  # Get data from Heroku app
    if response.status_code == 200:
        data = response.json()
        # In real case, you can filter records based on the 'name' or other criteria
        records = data.get("message", "No data available.")
        return jsonify(records)
    else:
        return jsonify({"message": "Failed to fetch data from the server."})

# Route to handle POST requests to send data to the Heroku API
@app.route('/send_data', methods=['POST'])
def send_data():
    # Get the data sent from the request (this could come from a form or external source like Raspberry Pi)
    data = request.json  # The JSON payload sent from Raspberry Pi
    headers = {'Content-Type': 'application/json'}

    # Send the data to the Heroku API (POST request)
    response = requests.post(heroku_url, json=data, headers=headers)

    if response.status_code == 200:
        return jsonify({"message": "Data sent successfully!"}), 200
    else:
        return jsonify({"message": "Failed to send data."}), 400

# Page for records specific to a name
@app.route('/record_page/<name>')
def record_page(name):
    return render_template('record_page.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
