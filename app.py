from flask import Flask, jsonify, request, render_template
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)

# PostgreSQL connection (Heroku automatically sets DATABASE_URL in environment variables)
DATABASE_URL = os.environ['DATABASE_URL']  # Heroku will set this automatically
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# Create the table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        sensor_id TEXT,
        temperature REAL,
        humidity REAL,
        timestamp TEXT
    );
""")
conn.commit()

@app.route('/')
def index():
    # Fetch all sensor data from the database to display on the webpage
    cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC;")
    data = cursor.fetchall()  # List of tuples (sensor_id, temperature, humidity, timestamp)
    return render_template("index.html", data=data)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    # Get JSON data from the request
    data = request.json

    # If no data is provided, return an error message
    if not data:
        return jsonify({"message": "No data provided or malformed JSON!"}), 400

    # Insert the received data into the PostgreSQL database
    cursor.execute("""
        INSERT INTO sensor_data (sensor_id, temperature, humidity, timestamp)
        VALUES (%s, %s, %s, %s);
    """, (data['sensor_id'], data['temperature'], data['humidity'], data['timestamp']))
    conn.commit()

    return jsonify({"message": "Data received successfully!"}), 200

@app.route('/get_data', methods=['GET'])
def get_data():
    # Return all the stored data in JSON format (for testing or other uses)
    cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC;")
    data = cursor.fetchall()
    result = [{"sensor_id": row[0], "temperature": row[1], "humidity": row[2], "timestamp": row[3]} for row in data]
    return jsonify({"data": result})

if __name__ == '__main__':
    app.run(debug=True)
