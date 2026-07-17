# migrate_json_to_sqlite.py
# One-time script to migrate existing data.json records to SQLite database

import json
import sqlite3
import os

JSON_FILE = "data.json"
DB_FILE = "grocery.db"

def migrate():
    """
    Reads records from data.json and populates the SQLite tables.
    """
    if not os.path.exists(JSON_FILE):
        print(f"No {JSON_FILE} found to migrate.")
        return
        
    with open(JSON_FILE, "r") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return
            
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Migrate Products
    products = data.get("products", {})
    products_migrated = 0
    product_name_to_id = {}
    
    for name, details in products.items():
        name_lower = name.lower()
        if isinstance(details, dict):
            price = details.get("price", 0.0)
            quantity = details.get("quantity", 0)
            category = details.get("category", "Other")
        elif isinstance(details, list):
            price = details[0] if len(details) > 0 else 0.0
            quantity = details[1] if len(details) > 1 else 0
            category = details[2] if len(details) > 2 else "Other"
        else:
            continue
            
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO products (name, price, quantity, category) VALUES (?, ?, ?, ?)",
                (name_lower, price, quantity, category)
            )
            # Retrieve the id
            cursor.execute("SELECT id FROM products WHERE name = ?", (name_lower,))
            pid = cursor.fetchone()[0]
            product_name_to_id[name_lower] = pid
            products_migrated += 1
        except Exception as e:
            print(f"Failed to migrate product {name}: {e}")
            
    # 2. Migrate Cart
    cart = data.get("cart", {})
    cart_migrated = 0
    for name, details in cart.items():
        name_lower = name.lower()
        if name_lower not in product_name_to_id:
            # Skip cart items without existing products
            continue
        pid = product_name_to_id[name_lower]
        quantity = details[1] if isinstance(details, list) else details.get("quantity", 0)
        try:
            cursor.execute(
                "INSERT OR REPLACE INTO cart (product_id, quantity) VALUES (?, ?)",
                (pid, quantity)
            )
            cart_migrated += 1
        except Exception as e:
            print(f"Failed to migrate cart item {name}: {e}")
            
    # 3. Migrate Orders & Order Items
    orders = data.get("orders", [])
    orders_migrated = 0
    order_items_migrated = 0
    
    for order in orders:
        oid = order.get("id")
        timestamp = order.get("timestamp")
        total = order.get("total", 0.0)
        
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO orders (id, timestamp, total) VALUES (?, ?, ?)",
                (oid, timestamp, total)
            )
            orders_migrated += 1
            
            for item in order.get("items", []):
                iname = item.get("item", "").lower()
                price = item.get("price", 0.0)
                qty = item.get("qty", 0)
                
                # Make sure the product exists in DB for foreign key constraint
                if iname not in product_name_to_id:
                    cursor.execute(
                        "INSERT OR IGNORE INTO products (name, price, quantity, category) VALUES (?, ?, ?, ?)",
                        (iname, price, 0, "Other")
                    )
                    cursor.execute("SELECT id FROM products WHERE name = ?", (iname,))
                    pid = cursor.fetchone()[0]
                    product_name_to_id[iname] = pid
                    
                pid = product_name_to_id[iname]
                cursor.execute(
                    "INSERT OR IGNORE INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                    (oid, pid, qty)
                )
                order_items_migrated += 1
        except Exception as e:
            print(f"Failed to migrate order {oid}: {e}")
            
    conn.commit()
    conn.close()
    
    print("Migration Summary:")
    print(f"- Products migrated: {products_migrated}")
    print(f"- Cart items migrated: {cart_migrated}")
    print(f"- Orders migrated: {orders_migrated}")
    print(f"- Order items migrated: {order_items_migrated}")

if __name__ == "__main__":
    # Ensure tables are created first
    import database
    migrate()
