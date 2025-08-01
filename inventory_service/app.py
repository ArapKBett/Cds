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
        sslmode='require'  # SSL required for Supabase etc.
    )
    return conn

def init_sample_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM inventory.products;")
    count = cursor.fetchone()[0]
    if count == 0:
        sample_products = [
            ("Laptop", 10, 1200.50),
            ("Smartphone", 25, 650.00),
            ("Wireless Mouse", 50, 25.99)
        ]
        cursor.executemany(
            "INSERT INTO inventory.products (name, stock, price) VALUES (%s, %s, %s)",
            sample_products
        )
        conn.commit()
        print("Inserted sample products.")
    cursor.close()
    conn.close()

@app.route('/')
def home():
    return "Inventory Service is running. Use /products to GET or POST product data.", 200

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM inventory.products ORDER BY id;")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(product) for product in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "stock", "price")):
        return jsonify({'error': 'Missing or invalid product data'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inventory.products (name, stock, price) VALUES (%s, %s, %s)",
        (data['name'], data['stock'], data['price'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product added'}), 201

if __name__ == '__main__':
    init_sample_products()
    app.run(debug=True, host='0.0.0.0', port=5002)
