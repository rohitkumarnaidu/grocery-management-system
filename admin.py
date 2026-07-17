# admin.py
# Admin-side business logic using SQLite database queries

import database

def add_product(item, price, quantity, category="Other"):
    if price < 0:
        return False, "Price cannot be negative"
    if quantity < 0:
        return False, "Quantity cannot be negative"
    data = database.load_data()
    item = item.lower()
    if "products" not in data:
        data["products"] = {}
    if item not in data["products"]:
        data["products"][item] = [price, quantity, category]
        database.save_data(data)
    """
    Adds a new product to the inventory database.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE name = ?", (item,))
        if cursor.fetchone():
            conn.close()
            return False, "Item already exists"
        cursor.execute(
            "INSERT INTO products (name, price, quantity, category) VALUES (?, ?, ?, ?)",
            (item, price, quantity, category)
        )
        conn.commit()
        conn.close()
        return True, "Item added successfully!"
    except Exception as e:
        return False, f"Database error: {e}"

def update_price(item, price):
    if price < 0:
        return False, "Price cannot be negative"
    data = database.load_data()
    item = item.lower()
    if item in data.get("products", {}):
        details = data["products"][item]
        # Check layout style to modify the value correctly
        if isinstance(details, list) and len(details) > 0:
            data["products"][item][0] = price
        elif isinstance(details, dict):
            data["products"][item]["price"] = price
            
        database.save_data(data)
    """
    Updates the price of an existing product in the inventory.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE name = ?", (item,))
        if not cursor.fetchone():
            conn.close()
            return False, "Product does not exist"
        cursor.execute("UPDATE products SET price = ? WHERE name = ?", (price, item))
        conn.commit()
        conn.close()
        return True, "Price updated successfully!"
    except Exception as e:
        return False, f"Database error: {e}"

def update_quantity(item, quantity):
    if quantity < 0:
        return False, "Quantity cannot be negative"
    data = database.load_data()
    item = item.lower()
    if item in data.get("products", {}):
        details = data["products"][item]
        # Check layout style to modify the value correctly
        if isinstance(details, list) and len(details) > 1:
            data["products"][item][1] = quantity
        elif isinstance(details, dict):
            data["products"][item]["quantity"] = quantity
            
        database.save_data(data)
    """
    Updates the stock quantity of an existing product in the inventory.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE name = ?", (item,))
        if not cursor.fetchone():
            conn.close()
            return False, "Product does not exist"
        cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", (quantity, item))
        conn.commit()
        conn.close()
        return True, "Quantity updated successfully!"
    except Exception as e:
        return False, f"Database error: {e}"

def delete_item(item):
    """
    Deletes a product from the database (also cascades deletes to cart).
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE name = ?", (item,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Product does not exist"
        pid = row['id']
        cursor.execute("DELETE FROM products WHERE id = ?", (pid,))
        conn.commit()
        conn.close()
        return True, "Deleted successfully!"
    except Exception as e:
        return False, f"Database error: {e}"

def get_low_stock_alerts(threshold=5):
    """
    Scans the inventory database and returns products with stock below threshold.
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, quantity, category FROM products WHERE quantity < ?", (threshold,))
        alerts = {}
        for row in cursor.fetchall():
            alerts[row['name']] = {
                "price": row['price'],
                "quantity": row['quantity'],
                "category": row['category'],
                "status": "Out of Stock" if row['quantity'] == 0 else "Low Stock"
            }
        conn.close()
        return alerts
    except Exception as e:
        print(f"Database error in get_low_stock_alerts: {e}")
        return {}

def verify_admin_login(input_password):
    """
    Verifies admin password using a secure SHA-256 hash check.
    """
    import hashlib
    correct_password = "admin123"
    stored_hash = hashlib.sha256(correct_password.encode('utf-8')).hexdigest()
    input_hash = hashlib.sha256(input_password.strip().encode('utf-8')).hexdigest()
    return input_hash == stored_hash

def get_sales_analytics():
    """
    Compiles sales analytics (total orders, total revenue, popular items, category breakdown).
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # 1. Total orders and total revenue
        cursor.execute("SELECT SUM(total), COUNT(id) FROM orders")
        row = cursor.fetchone()
        total_revenue = row[0] if row[0] is not None else 0.0
        total_orders = row[1] if row[1] is not None else 0
        
        # 2. Popular items (best sellers)
        cursor.execute("""
            SELECT p.name, SUM(oi.quantity) as qty_sold
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            GROUP BY oi.product_id
            ORDER BY qty_sold DESC
        """)
        best_sellers = [{"item": row['name'], "quantity_sold": row['qty_sold']} for row in cursor.fetchall()]
        
        # 3. Category revenue breakdown
        cursor.execute("""
            SELECT p.category, SUM(oi.quantity * p.price) as cat_revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            GROUP BY p.category
        """)
        category_revenue = {row['category']: round(row['cat_revenue'], 2) for row in cursor.fetchall()}
        
        conn.close()
        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "best_selling_products": best_sellers,
            "revenue_by_category": category_revenue
        }
    except Exception as e:
        print(f"Database error in get_sales_analytics: {e}")
        return {
            "total_revenue": 0.0,
            "total_orders": 0,
            "best_selling_products": [],
            "revenue_by_category": {}
        }
    # Sort best sellers list by total quantity sold (highest to lowest)
    best_sellers = sorted(
        [{"item": k, "quantity_sold": v} for k, v in product_counts.items()],
        key=lambda x: x["quantity_sold"],
        reverse=True
    )
    
    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "best_selling_products": best_sellers,
        "revenue_by_category": {k: round(v, 2) for k, v in category_revenue.items()}
    }
def add_coupon(code, discount_type, value, min_purchase=0.0):
    """
    Creates a coupon code.
    discount_type: 'percentage' (e.g., 10 for 10% off) or 'flat' (e.g., 50 for Rs.50 off)
    """
    data = database.load_data()
    if "coupons" not in data:
        data["coupons"] = {}
        
    code_upper = code.strip().upper()
    data["coupons"][code_upper] = {
        "type": discount_type.lower(),
        "value": float(value),
        "min_purchase": float(min_purchase)
    }
    database.save_data(data)
    return True, f"Coupon '{code_upper}' added successfully!"

def delete_coupon(code):
    data = database.load_data()
    code_upper = code.strip().upper()
    if "coupons" in data and code_upper in data["coupons"]:
        del data["coupons"][code_upper]
        database.save_data(data)
        return True, f"Coupon '{code_upper}' deleted successfully!"
    return False, "Coupon code does not exist"

def get_active_coupons():
    data = database.load_data()
    return data.get("coupons", {})
