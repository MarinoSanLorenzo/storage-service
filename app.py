from flask import Flask, request, jsonify
import datetime
import sqlite3, requests, datetime
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

@app.route('/api/display_nb_kcal_today', methods=['GET'])
def display_nb_kcal_today():
    try:
        conn = sqlite3.connect('kcal_tracker.db')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute a query to fetch data
        cursor.execute("SELECT SUM(kcal) as total_kcal FROM kcal_entries \
                    WHERE DATE(date) = DATE('now', 'localtime');")

        # Fetch all rows from the result set
        rows = cursor.fetchall() # output [()] List[Tuple[Union[str, None]]]

        total_kcal = rows[0][0]
        if total_kcal is None:
            total_kcal = 0
        
        # web_kcal_manager_service_url = 'http://20.123.77.86:80/api/display_total_kcal'# public ip address and http port of the web vm in Azure

        return jsonify({'total_kcal': total_kcal}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # try:
        
    #     # response = requests.post(web_kcal_manager_service_url, data_to_send_back_to_web_kcal_manager_service)
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
        


@app.route('/api/display_kcal', methods=['GET'])
def display_kcal():
    return jsonify({'nb_kcal':1}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


# #curl -d "{\"kcal\":\"3500\"}" http://localhost:5000/api/store_kcal -H "Content-Type: application/json"
# sudo -E python3 main.py