from flask import Flask, jsonify, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

# Function to load data from SQLite into a DataFrame
def load_data_from_sqlite(db_file, table_name):
    conn = sqlite3.connect(db_file)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert the data to a JSON format
    json_data = df.to_json(orient='records', force_ascii=False)

    print(json_data)

    return json_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    # Load data from SQLite into a DataFrame
    db_file = "car_data.db"
    table_name = "car_data"
    json_data = load_data_from_sqlite(db_file, table_name)
    
    
    # Return JSON data
    return json_data

if __name__ == '__main__':
    app.run(debug=True)