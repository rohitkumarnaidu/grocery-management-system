# admin.py
# Admin-side business logic using SQLite database queries

import database

def add_product(item, price, quantity, category="Other", image_url=""):
    """
    Adds a new product to the inventory database.
    """
    item = item.strip().lower()
    if price < 0:
        return False, "Price cannot be negative"
    if quantity < 0:
        return False, "Quantity cannot be negative"
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE name = ?", (item,))
        if cursor.fetchone():
            conn.close()
            return False, "Item already exists"
        cursor.execute(
            "INSERT INTO products (name, price, quantity, category, image_url) VALUES (?, ?, ?, ?, ?)",
            (item, price, quantity, category, image_url)
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
    if price < 0:
        return False, "Price cannot be negative"
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
    if quantity < 0:
        return False, "Quantity cannot be negative"
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

def archive_product(item):
    """
    Archives a product by setting its archived flag to 1 (soft-delete).
    Archived products are hidden from the active inventory and the customer shop,
    but their data is preserved and can be restored at any time.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, archived FROM products WHERE name = ?", (item,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Product does not exist"
        if row['archived'] == 1:
            conn.close()
            return False, "Product is already archived"
        cursor.execute("UPDATE products SET archived = 1 WHERE name = ?", (item,))
        conn.commit()
        conn.close()
        return True, "Product archived successfully!"
    except Exception as e:
        return False, f"Database error: {e}"

def restore_product(item):
    """
    Restores an archived product by setting its archived flag back to 0.
    The product will reappear in the active inventory and the customer shop.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, archived FROM products WHERE name = ?", (item,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Product does not exist"
        if row['archived'] == 0:
            conn.close()
            return False, "Product is not archived"
        cursor.execute("UPDATE products SET archived = 0 WHERE name = ?", (item,))
        conn.commit()
        conn.close()
        return True, "Product restored successfully!"
    except Exception as e:
        return False, f"Database error: {e}"

def permanently_delete_product(item):
    """
    Permanently deletes a product from the database.
    Only works on products that are already archived as a safety guard.
    This action is irreversible.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, archived FROM products WHERE name = ?", (item,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Product does not exist"
        if row['archived'] == 0:
            conn.close()
            return False, "Product must be archived before it can be permanently deleted"
        pid = row['id']
        cursor.execute("DELETE FROM products WHERE id = ?", (pid,))
        conn.commit()
        conn.close()
        return True, "Product permanently deleted!"
    except Exception as e:
        return False, f"Database error: {e}"

def get_low_stock_alerts(threshold=5):
    """
    Scans the inventory database and returns products with stock below threshold.
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, price, quantity, category FROM products WHERE quantity < ? AND archived = 0", (threshold,))
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
    Compiles sales analytics including:
    - Total orders and total revenue
    - Best-selling products
    - Revenue by category (dict)
    - revenue_last_7_days: [{date, revenue}] for the last 7 calendar days
    - quantity_by_category: [{category, quantity}] for pie chart
    """
    from datetime import datetime, timedelta

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

        # 4. Revenue per day for the last 7 days (for Line Chart)
        # Orders store timestamps as ISO strings; extract the date portion for grouping.
        cursor.execute("""
            SELECT substr(timestamp, 1, 10) as order_date, SUM(total) as daily_revenue
            FROM orders
            WHERE timestamp >= date('now', '-6 days')
            GROUP BY order_date
            ORDER BY order_date ASC
        """)
        daily_rows = {row['order_date']: round(row['daily_revenue'], 2) for row in cursor.fetchall()}

        # Build a complete 7-day list, filling zeros for missing days
        today = datetime.utcnow().date()
        revenue_last_7_days = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_str = day.isoformat()          # "YYYY-MM-DD"
            label = day.strftime("%b %d")       # "Jul 22" — readable X-axis label
            revenue_last_7_days.append({
                "date": label,
                "revenue": daily_rows.get(day_str, 0.0)
            })

        # 5. Total quantity sold per category (for Pie Chart)
        cursor.execute("""
            SELECT p.category, SUM(oi.quantity) as qty_sold
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            GROUP BY p.category
            ORDER BY qty_sold DESC
        """)
        quantity_by_category = [
            {"category": row['category'], "quantity": row['qty_sold']}
            for row in cursor.fetchall()
        ]

        conn.close()
        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "best_selling_products": best_sellers,
            "revenue_by_category": category_revenue,
            "revenue_last_7_days": revenue_last_7_days,
            "quantity_by_category": quantity_by_category
        }
    except Exception as e:
        print(f"Database error in get_sales_analytics: {e}")
        return {
            "total_revenue": 0.0,
            "total_orders": 0,
            "best_selling_products": [],
            "revenue_by_category": {},
            "revenue_last_7_days": [],
            "quantity_by_category": []
        }
