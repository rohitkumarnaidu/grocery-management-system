import sqlite3
import os

DB_FILE = "grocery.db"

def get_db_connection():
    """
    Establishes a connection to the SQLite database.
    Enforces foreign key checks and row factory for named columns.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes the SQLite tables with primary keys, types, and foreign key relationships.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        category TEXT NOT NULL,
        is_archived INTEGER DEFAULT 0
    );
    """)
    
    # Check if is_archived column exists, add if not (for migration)
    cursor.execute("PRAGMA table_info(products)")
    columns = [col['name'] for col in cursor.fetchall()]
    if 'is_archived' not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN is_archived INTEGER DEFAULT 0")
    
    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        total REAL NOT NULL
    );
    """)
    
    # Order Items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_id TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        PRIMARY KEY (order_id, product_id),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );
    """)
    
    # Cart table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        product_id INTEGER PRIMARY KEY,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    conn.close()

# Helper queries to keep app.py and modules clean
def get_all_products(include_archived=False):
    """
    Returns products in the dictionary format expected by the frontend.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if include_archived:
        cursor.execute("SELECT name, price, quantity, category, is_archived FROM products")
    else:
        cursor.execute("SELECT name, price, quantity, category, is_archived FROM products WHERE is_archived = 0")
    products = {}
    for row in cursor.fetchall():
        products[row['name']] = [row['price'], row['quantity'], row['category'], row['is_archived']]
    conn.close()
    return products

def get_all_orders():
    """
    Returns orders in the hierarchical list format expected by the frontend.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, total FROM orders ORDER BY timestamp DESC")
    orders = []
    order_rows = cursor.fetchall()
    for o in order_rows:
        cursor.execute("""
            SELECT p.name, p.price, oi.quantity 
            FROM order_items oi 
            JOIN products p ON oi.product_id = p.id 
            WHERE oi.order_id = ?
        """, (o['id'],))
        items = [{"item": row['name'], "price": row['price'], "qty": row['quantity']} for row in cursor.fetchall()]
        orders.append({
            "id": o['id'],
            "timestamp": o['timestamp'],
            "items": items,
            "total": o['total']
        })
    conn.close()
    return orders

def get_cart():
    """
    Returns the cart in the dictionary format expected by the frontend.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, p.price, c.quantity 
        FROM cart c 
        JOIN products p ON c.product_id = p.id
    """)
    cart = {}
    for row in cursor.fetchall():
        cart[row['name']] = [row['price'], row['quantity']]
    conn.close()
    return cart

# Automatically run initialization on load/import
init_db()