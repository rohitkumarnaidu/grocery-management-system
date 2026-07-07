from flask import Flask, request, jsonify
from flask_cors import CORS
import admin
import customer
import database

app = Flask(__name__)
CORS(app)

# SECURING ALL ENDPOINTS WITH A SIMPLE PASSWORD GUARD FOR ADMIN ROUTES
@app.before_request
def authenticate_admin():
    # Only check requests targeting the admin product modification API routes
    if request.path.startswith('/api/products') and request.method != 'GET':
        admin_password = request.headers.get('X-Admin-Password')
        # Simple password guard matching the original concept's requirement
        if admin_password != 'admin123':
            return jsonify({"success": False, "message": "Unauthorized: Invalid or missing admin password"}), 401

@app.route('/')
def index():
    return jsonify({"status": "API is running"})

# --- Admin API ---

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(admin.get_inventory())

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    category = data.get('category', 'Other')
    try:
        price = float(data['price'])
        quantity = int(data['qty'])  # Kept 'qty' for incoming frontend key compatibility
        if price < 0 or quantity < 0:
            return jsonify({"success": False, "message": "Price and quantity cannot be negative"}), 400
    except (ValueError, TypeError, KeyError):
        return jsonify({"success": False, "message": "Invalid input: Price must be a number and Quantity must be an integer"}), 400
    success, message = admin.add_product(data['item'], price, quantity, category)
    return jsonify({"success": success, "message": message})

@app.route('/api/products/<item>/price', methods=['PUT'])
def update_price(item):
    data = request.json
    try:
        price = float(data['price'])
        if price < 0:
            return jsonify({"success": False, "message": "Price cannot be negative"}), 400
    except (ValueError, TypeError, KeyError):
        return jsonify({"success": False, "message": "Invalid input: Price must be a valid number"}), 400
    success, message = admin.update_price(item, price)
    return jsonify({"success": success, "message": message})

@app.route('/api/products/<item>/qty', methods=['PUT'])
def update_qty(item):
    data = request.json
    try:
        quantity = int(data['qty'])
        if quantity < 0:
            return jsonify({"success": False, "message": "Quantity cannot be negative"}), 400
    except (ValueError, TypeError, KeyError):
        return jsonify({"success": False, "message": "Invalid input: Quantity must be a valid integer"}), 400
    success, message = admin.update_quantity(item, quantity)
    return jsonify({"success": success, "message": message})

@app.route('/api/products/<item>', methods=['DELETE'])
def delete_product(item):
    success, message = admin.delete_item(item)
    return jsonify({"success": success, "message": message})

# --- Customer API ---

@app.route('/api/cart', methods=['GET'])
def get_cart():
    cart = customer.get_cart()
    total_price = customer.view_total_price()  
    return jsonify({"cart": cart, "total_price": total_price})

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    try:
        quantity = int(data['qty'])
        if quantity <= 0:
            return jsonify({"success": False, "message": "Quantity must be greater than zero"}), 400
    except (ValueError, TypeError, KeyError):
        return jsonify({"success": False, "message": "Invalid input: Quantity must be a valid integer"}), 400
    success, message = customer.add_item(data['item'], quantity)
    return jsonify({"success": success, "message": message})

@app.route('/api/cart/<item>', methods=['PUT'])
def update_cart_qty(item):
    data = request.json
    try:
        quantity = int(data['qty'])
    except (ValueError, TypeError, KeyError):
        return jsonify({"success": False, "message": "Invalid input: Quantity must be a valid integer"}), 400
    success, message = customer.update_item_qty(item, quantity)
    return jsonify({"success": success, "message": message})

@app.route('/api/cart/<item>', methods=['DELETE'])
def remove_from_cart(item):
    success, message = customer.delete_item(item)
    return jsonify({"success": success, "message": message})

@app.route('/api/checkout', methods=['POST'])
def checkout():
    success, message = customer.checkout()
    return jsonify({"success": success, "message": message})

@app.route('/api/orders', methods=['GET'])
def get_orders():
    data = database.load_data()
    orders = data.get("orders", [])
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)