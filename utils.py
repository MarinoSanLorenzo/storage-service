# Function to initialize the SQLite database
import sqlite3


def initialize_database():
    conn = sqlite3.connect('kcal_tracker.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS kcal_entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, kcal INTEGER)''')
    conn.commit()
    conn.close()
