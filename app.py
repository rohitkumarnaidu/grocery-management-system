from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import false
import admin
import customer
import database

app = Flask(__name__)
CORS(app)

# SECURING ALL ENDPOINTS WITH A SIMPLE PASSWORD GUARD FOR ADMIN ROUTES
@app.before_request
def authenticate_admin():
    if request.path.startswith('/api/products') and request.method != 'GET':
        admin_password = request.headers.get('X-Admin-Password')
        
        # if admin_password != 'admin123':
        #     return jsonify({"success": False, "message": "Unauthorized: Invalid or missing admin password"}), 401

        # Fallback to the original plaintext check to keep Issue #11 isolated and functional
        if admin_password != 'admin123':
            return jsonify({"success": False, "message": "Unauthorized: Invalid or missing admin password"}), 401     
@app.route('/')
def index():
    return jsonify({"status": "API is running"})

# --- Admin API ---

@app.route('/api/products', methods=['GET'])
def get_products():
    # Fetch data safely from the central database schema
    data = database.load_data()
    return jsonify(data.get("products", {}))

# Track failed login attempts globally
failed_attempts = 0

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    global failed_attempts
    
    # lock out if attempts are exceeded
    if failed_attempts >= 3:
        return jsonify({"success": False, "message": "Access Denied. Account locked due to too many failed attempts."}), 403
        
    data = request.get_json() or {}
    password = data.get("password", "")
    
    if admin.verify_admin_login(password):
        failed_attempts = 0 # Reset on success
        return jsonify({"success": True, "message": "Access Granted. Welcome Admin."})
    else:
        failed_attempts += 1
        remaining = 3 - failed_attempts
        if failed_attempts >= 3:
            return jsonify({"success": False, "message": "Access Denied. Account locked."}), 403
        return jsonify({"success": False, "message": f"Invalid password. {remaining} attempts remaining."}), 401

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

@app.route('/api/admin/alerts', methods=['GET'])
def get_low_stock_alerts():
    threshold = request.args.get('threshold', default=5, type=int)
    alerts = admin.get_low_stock_alerts(threshold)
    return jsonify(alerts)

@app.route('/api/admin/analytics', methods=['GET'])
def get_sales_analytics():
    analytics = admin.get_sales_analytics()
    return jsonify(analytics)


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

# --- Search & Filter API ---
@app.route('/api/products/filter', methods=['GET'])
def search_products():
    
    query_name = request.args.get('name', default=None, type=str)
    category = request.args.get('category', default=None, type=str)
    min_price = request.args.get('min_price', default=None, type=float)
    max_price = request.args.get('max_price', default=None, type=float)
    
    results = customer.search_and_filter_products(
        query_name=query_name, 
        min_price=min_price, 
        max_price=max_price, 
        category=category
    )
    return jsonify(results)
if __name__ == '__main__':
    app.run(debug=True)