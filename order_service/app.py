from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    'user': os.environ.get('MYSQL_USER', 'flask_user'),
    'password': os.environ.get('MYSQL_PASSWORD', 'flask_password'),
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'database': os.environ.get('MYSQL_DATABASE', 'order_db')
}

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (product_id, quantity, price) VALUES (%s, %s, %s)",  
                   (data['product_id'], data['quantity'], data['price']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Order placed'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10001)
  
