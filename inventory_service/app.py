from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory sample products data for testing without DB
sample_products = [
    {"id": 1, "name": "Laptop", "stock": 10, "price": 1200.50},
    {"id": 2, "name": "Smartphone", "stock": 25, "price": 650.00},
    {"id": 3, "name": "Wireless Mouse", "stock": 50, "price": 25.99}
]

# Landing page route
@app.route('/')
def home():
    return "Inventory Service is running with in-memory products. Use /products endpoint.", 200

# GET all products route - returns the in-memory list
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(sample_products)

# POST a new product - adds to the in-memory list
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "stock", "price")):
        return jsonify({'error': 'Missing or invalid product data'}), 400

    new_id = max(p["id"] for p in sample_products) + 1 if sample_products else 1
    new_product = {
        "id": new_id,
        "name": data["name"],
        "stock": data["stock"],
        "price": data["price"]
    }
    sample_products.append(new_product)
    return jsonify({'message': 'Product added', 'product': new_product}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
