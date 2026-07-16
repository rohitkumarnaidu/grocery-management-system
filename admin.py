# admin.py
# Admin-side business logic using SQLite database queries

import database

def add_product(item, price, quantity, category="Other"):
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