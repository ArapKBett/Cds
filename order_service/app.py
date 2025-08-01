from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB', 'postgres'),
        user=os.environ.get('POSTGRES_USER', 'postgres'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('POSTGRES_HOST'),
        port=os.environ.get('POSTGRES_PORT', 5432),
        sslmode='require'
    )
    return conn

@app.route('/')
def home():
    return "Order Service is running. Use /orders to GET or POST order data.", 200

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM orders.orders ORDER BY id;")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(order) for order in orders])

@app.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    if not data or not all(k in data for k in ("product_id", "quantity", "price")):
        return jsonify({'error': 'Missing or invalid order data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders.orders (product_id, quantity, price) VALUES (%s, %s, %s)",
        (data['product_id'], data['quantity'], data['price'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Order placed'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
