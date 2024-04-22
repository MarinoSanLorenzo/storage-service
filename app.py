from flask import Flask, request, jsonify
import datetime
import sqlite3
from utils import initialize_database
app = Flask(__name__)


# Initialize the database when the application starts
initialize_database()

# API endpoint to store kcal data
@app.route('/api/store_kcal', methods=['POST'])
def store_kcal():
    data = request.get_json()
    date = datetime.datetime.now()
    kcal = data.get('kcal')
    
    if not date or not kcal:
        return jsonify({'error': 'Date and kcal are required parameters'}), 400
    
    try:
        conn = sqlite3.connect('kcal_tracker.db')
        c = conn.cursor()
        c.execute("INSERT INTO kcal_entries (date, kcal) VALUES (?, ?)", (date, kcal))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Kcal data stored successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/display_kcal', methods=['GET'])
def display_kcal():
    return jsonify({'nb_kcal':1}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


# #curl -d "{\"kcal\":\"3500\"}" http://localhost:5000/api/store_kcal -H "Content-Type: application/json"
# sudo -E python3 main.py