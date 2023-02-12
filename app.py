from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def create_Database():
    sql_query = """ CREATE TABLE measurements (
        id integer PRIMARY KEY,
        time DATETIME DEFAULT CURRENT_TIMESTAMP,
        ip_address text NOT NULL,
        value integer NOT NULL
    )"""
    delete_Database = "DROP TABLE measurements"
    connection = sqlite3.connect('measurements.sqlite')
    cursor = connection.cursor()
    cursor.execute(sql_query)
    #cursor.execute(delete_Database)
#create_Database()


def db_connection():
    connection = sqlite3.connect('measurements.sqlite')
    return connection


@app.route('/api/measurements', methods=['POST', 'GET', 'DELETE'])
def post_Measurements():
    connection = db_connection()
    cursor = connection.cursor()
    if request.method == 'GET':
        return jsonify(cursor.execute("SELECT * FROM measurements").fetchall())
    
    if request.method == 'POST':
        ip_address = request.args.get('address')
        value = request.args.get('value')
        
        
        id_number = cursor.execute("SELECT max(id) FROM measurements").fetchall()
     
        if id_number[0][0] == None:
            cursor.execute(f"INSERT INTO measurements VALUES (0,CURRENT_TIME,'0.0.0.0',0)")

        id_number = cursor.execute("SELECT max(id) FROM measurements").fetchall()
        id_number = id_number[0][0] + 1
        cursor.execute(f"INSERT INTO measurements VALUES ({id_number},CURRENT_TIME,{ip_address},{value})")
        connection.commit()
        return "OK"

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM measurements")
        connection.commit()
        return "OK"

@app.route('/api/top100')
def get_last100():
    connection = db_connection()
    cursor = connection.cursor()
    return jsonify(cursor.execute("SELECT * FROM measurements ORDER BY id DESC LIMIT 100").fetchall())


@app.route('/api/measurements/byip')
def get_Ip_Address():
    connection = db_connection()
    cursor = connection.cursor()

    ip_address = request.args.get('address')
    return jsonify(cursor.execute(f"SELECT * FROM measurements WHERE ip_address = {ip_address}").fetchall())


@app.route('/api/stats')
def get_stats():
    connection = db_connection()
    cursor = connection.cursor()

    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")

    mean = cursor.execute(f"SELECT avg(value) FROM measurements WHERE time BETWEEN {startDate} AND {endDate}").fetchall()
    highest = cursor.execute(f"SELECT max(value) FROM measurements WHERE time BETWEEN {startDate} AND {endDate}").fetchall()
    lowest = cursor.execute(f"SELECT min(value) FROM measurements WHERE time BETWEEN {startDate} AND {endDate}").fetchall()
    return {'mean': mean[0][0],'highest': highest[0][0],'lowest': lowest[0][0]}



if __name__ == '__main__':
    app.run(debug=True)