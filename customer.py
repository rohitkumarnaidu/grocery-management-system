# customer.py
# Customer-side business logic using SQLite database queries

import database
import time
import uuid
import os

def get_cart():
    """
    Retrieves all items currently in the cart.
    """
    try:
        return database.get_cart()
    except Exception as e:
        print(f"Database error in get_cart: {e}")
        return {}

def add_item(item, quantity):
    if quantity <= 0:
        return False, "Quantity must be greater than zero"
    data = database.load_data()
    item = item.lower()
    
    # using 'products' in place of 'prod'
    if item not in data.get("products", {}):
        return False, "Product does not exist in inventory"
        
    # UPDATED: Swapped out indices [0] and [1] for self-documenting dictionary keys
    price = data["products"][item]["price"]
    available_stock = data["products"][item]["quantity"]
    
    # Track what is already sitting in the cart
    current_cart_qty = 0
    if "cart" in data and item in data["cart"]:
        current_cart_qty = data["cart"][item][1]
        
    # Stock Validation Guard
    if current_cart_qty + quantity > available_stock:
        return False, f"Cannot add quantity. Only {available_stock} items available in stock, and you have {current_cart_qty} in your cart."
    """
    Adds a specified quantity of a product to the cart.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # Check product existence and available stock
        cursor.execute("SELECT id, price, quantity FROM products WHERE name = ?", (item,))
        prod = cursor.fetchone()
        if not prod:
            conn.close()
            return False, "Product does not exist in inventory"
            
        pid = prod['id']
        available_stock = prod['quantity']
        
        # Check current cart quantity
        cursor.execute("SELECT quantity FROM cart WHERE product_id = ?", (pid,))
        cart_row = cursor.fetchone()
        current_cart_qty = cart_row['quantity'] if cart_row else 0
        
        if current_cart_qty + quantity > available_stock:
            conn.close()
            return False, f"Cannot add quantity. Only {available_stock} items available in stock, and you have {current_cart_qty} in your cart."
            
        if cart_row:
            cursor.execute("UPDATE cart SET quantity = quantity + ? WHERE product_id = ?", (quantity, pid))
        else:
            cursor.execute("INSERT INTO cart (product_id, quantity) VALUES (?, ?)", (pid, quantity))
            
        conn.commit()
        conn.close()
        return True, "Added to cart"
    except Exception as e:
        return False, f"Database error in add_item: {e}"

def delete_item(item):
    """
    Deletes a product completely from the cart.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE name = ?", (item,))
        prod = cursor.fetchone()
        if not prod:
            conn.close()
            return False, "Product not in cart"
        pid = prod['id']
        
        cursor.execute("SELECT quantity FROM cart WHERE product_id = ?", (pid,))
        if not cursor.fetchone():
            conn.close()
            return False, "Product not in cart"
            
        cursor.execute("DELETE FROM cart WHERE product_id = ?", (pid,))
        conn.commit()
        conn.close()
        return True, "Deleted from cart"
    except Exception as e:
        return False, f"Database error in delete_item: {e}"

def update_item_qty(item, quantity):
    """
    Updates the quantity of a product in the cart.
    Removes the item if quantity drops to 0 or below.
    """
    item = item.strip().lower()
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, quantity FROM products WHERE name = ?", (item,))
        prod = cursor.fetchone()
        if not prod:
            conn.close()
            return False, "Item not in cart"
        pid = prod['id']
        available_stock = prod['quantity']
        
        cursor.execute("SELECT quantity FROM cart WHERE product_id = ?", (pid,))
        cart_row = cursor.fetchone()
        if not cart_row:
            conn.close()
            return False, "Item not in cart"
            
        if quantity <= 0:
            cursor.execute("DELETE FROM cart WHERE product_id = ?", (pid,))
            conn.commit()
            conn.close()
            return True, f"Removed '{item}' from cart."
            
        # Check stock bounds
        if quantity > available_stock:
            conn.close()
            return False, f"Cannot update quantity. Only {available_stock} items available in stock."
            
        cursor.execute("UPDATE cart SET quantity = ? WHERE product_id = ?", (quantity, pid))
        conn.commit()
        conn.close()
        return True, f"Updated '{item}' quantity to {quantity}."
    except Exception as e:
        return False, f"Database error in update_item_qty: {e}"

def view_total_price():
    """
    Computes total price of items currently in the cart.
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(c.quantity * p.price) 
            FROM cart c 
            JOIN products p ON c.product_id = p.id
        """)
        row = cursor.fetchone()
        total = row[0] if row[0] is not None else 0.0
        conn.close()
        return total
    except Exception as e:
        print(f"Database error in view_total_price: {e}")
        return 0.0

def checkout():
    """
    Performs checkout: validates inventory, deducts stock, creates orders, and clears cart.
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        # Fetch cart items with product details
        cursor.execute("""
            SELECT c.product_id, c.quantity, p.name, p.price, p.quantity as stock
            FROM cart c
            JOIN products p ON c.product_id = p.id
        """)
        cart_items = cursor.fetchall()
        if not cart_items:
            conn.close()
            return False, "Cart is empty"
            
        # Stock verification check
        unavailable_items = []
        for item in cart_items:
            if item['stock'] < item['quantity']:
                unavailable_items.append(item['name'])
                
        if unavailable_items:
            conn.close()
            return False, f"Checkout failed. The following items went out of stock or have insufficient inventory: {', '.join(unavailable_items)}. Please adjust your cart."
            
        # Insert orders, order items, and deduct stock
        total = 0.0
        items_list = []
        order_id = str(uuid.uuid4())[:8].upper()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        for item in cart_items:
            item_total = item['price'] * item['quantity']
            total += item_total
            # Deduct stock
            cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (item['quantity'], item['product_id']))
            # Add to receipt items
            items_list.append({"item": item['name'], "price": item['price'], "qty": item['quantity']})
            
        # Insert Order
        cursor.execute("INSERT INTO orders (id, timestamp, total) VALUES (?, ?, ?)", (order_id, timestamp, total))
        
        # Insert Order Items
        for item in cart_items:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", (order_id, item['product_id'], item['quantity']))
            
        # Clear Cart
        cursor.execute("DELETE FROM cart")
def checkout(coupon_code=None):
    data = database.load_data()
    cart = data.get("cart", {})
    
    if not cart:
        return False, "Cart is empty"
        
    prod = data.get("products", {})
    subtotal = 0
    items_list = []
    
    unavailable_items = []
    for item, details in cart.items():
        quantity = details[1] if isinstance(details, list) else details.get("quantity", 0)
        if item not in prod or prod[item]["quantity"] < quantity:
            unavailable_items.append(item)
            
    if unavailable_items:
        return False, f"Checkout failed. Insufficient stock for: {', '.join(unavailable_items)}."
            
    for item, details in cart.items():
        price = details[0] if isinstance(details, list) else details.get("price", 0.0)
        quantity = details[1] if isinstance(details, list) else details.get("quantity", 0)
        
        # --- Optional Bulk-Buy Logic (Buy 3 get 1 free style calculation if item matches a rule) ---
        # If buying 3 or more of the same item, charge for quantity - (quantity // 4)
        if quantity >= 4:
            billable_qty = quantity - (quantity // 4)
            subtotal += price * billable_qty
        else:
            subtotal += price * quantity
            
        prod[item]["quantity"] -= quantity
        items_list.append({"item": item, "price": price, "qty": quantity})
        
    # Apply promotional coupons if supplied
    discount_amount = 0.0
    if coupon_code:
        is_valid, result = validate_coupon(coupon_code, subtotal)
        if not is_valid:
            return False, f"Checkout aborted: {result}"
        discount_amount = result
        
    total = max(0.0, subtotal - discount_amount)
    order_id = str(uuid.uuid4())[:8].upper()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    order = {
        "id": order_id,
        "timestamp": timestamp,
        "items": items_list,
        "subtotal": round(subtotal, 2),
        "coupon_applied": coupon_code.upper() if coupon_code else None,
        "discount_applied": discount_amount,
        "total": round(total, 2)
    }
    
    if "orders" not in data:
        data["orders"] = []
        
        conn.commit()
        conn.close()
        
        order = {
            "id": order_id,
            "timestamp": timestamp,
            "items": items_list,
            "total": total
        }
        
        receipt_path = generate_receipt_file(order)
        return True, f"Checkout successful! Invoice generated at {receipt_path}. Total: Rs.{order['total']}"
    except Exception as e:
        return False, f"Database error during checkout: {e}"

def search_and_filter_products(query_name=None, min_price=None, max_price=None, category=None):
    """
    Searches and filters products using SQLite query parameters.
    """
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT name, price, quantity, category FROM products WHERE 1=1"
        params = []
        
        if query_name:
            query += " AND name LIKE ?"
            params.append(f"%{query_name.lower()}%")
        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        if category:
            query += " AND category = ?"
            params.append(category)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        results = {}
        for row in rows:
            results[row['name']] = [row['price'], row['quantity'], row['category']]
        conn.close()
        return results
    except Exception as e:
        print(f"Database error in search_and_filter_products: {e}")
        return {}

def generate_receipt_file(order):
    """
    Generates a clean, beautifully aligned text-based invoice.
    Saves it to disk under the 'receipts/' folder for secure record-keeping.
    """
    os.makedirs("receipts", exist_ok=True)
    filename = f"receipts/receipt_{order['id']}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=========================================\n")
        f.write("          GROCERY MANAGEMENT SYSTEM      \n")
        f.write("=========================================\n")
        f.write(f"Order ID   : {order['id']}\n")
        f.write(f"Date/Time  : {order['timestamp']}\n")
        f.write("-----------------------------------------\n")
        f.write(f"{'Item':<18} {'Qty':<5} {'Price':<8} {'Total':<8}\n")
        f.write("-----------------------------------------\n")
        
        for item in order["items"]:
            name = item["item"].strip().capitalize()
            if len(name) > 16:
                name = name[:13] + "..."
                
            qty = item["qty"]
            price = item["price"]
            item_total = price * qty
            
            f.write(f"{name:<18} {qty:<5} Rs.{price:<5.2f} Rs.{item_total:<6.2f}\n")
            
        f.write("-----------------------------------------\n")
        f.write(f"{'Grand Total':<30} Rs.{order['total']:.2f}\n")
        f.write("=========================================\n")
        f.write("        Thank you for shopping with us!   \n")
        f.write("=========================================\n")
        
    return filename
