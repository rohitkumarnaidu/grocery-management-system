import database
import time
import uuid

def get_cart():
    data = database.load_data()
    return data.get("cart", {})
    
    database.save_data(data)
    return data.get("cart", {})

def add_item(item, quantity):
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
        
    if "cart" not in data:
        data["cart"] = {}
        
    if item in data["cart"]:
        data["cart"][item][1] += quantity
    else:
        data["cart"][item] = [price, quantity]
        
    database.save_data(data)
    return True, "Added to cart"

def delete_item(item):
    data = database.load_data()
    item = item.strip().lower()
    if item in data.get("cart", {}):
        del data["cart"][item]
        database.save_data(data)
        return True, "Deleted from cart"
    return False, "Product not in cart"

def update_item_qty(item, quantity):
    """
    Updates the quantity of an item in the cart.
    Safely handles checks to prevent KeyError crashes on non-existent items.
    """
    data = database.load_data()
    cart = data.get("cart", {})
    
    # --- BUGFIX #4: Existence Check Guard ---
    if item not in cart:
        return False, "Item not in cart"
        
    # Handle removal safely if quantity drops to zero or below
    if quantity <= 0:
        del cart[item]
        database.save_data(data)
        return True, f"Removed '{item}' from cart."
    if isinstance(cart[item], list) and len(cart[item]) > 1:
        cart[item][1] = quantity
    elif isinstance(cart[item], dict):
        cart[item]["quantity"] = quantity
        
    database.save_data(data)
    return True, f"Updated '{item}' quantity to {quantity}."

def view_total_price():
    data = database.load_data()
    cart = data.get("cart", {})
    # Safely handles both list and dictionary schemas to prevent TypeErrors
    total_price = 0
    for item in cart:
        if isinstance(cart[item], list):
            total_price += cart[item][0] * cart[item][1]
        elif isinstance(cart[item], dict):
            total_price += cart[item].get("price", 0) * cart[item].get("quantity", 0)
    return total_price

def checkout():
    data = database.load_data()
    cart = data.get("cart", {})
    
    if not cart:
        return False, "Cart is empty"
        
    prod = data.get("products", {})
    total = 0
    items_list = []
    
    unavailable_items = []
    for item, details in cart.items():
        # Safely extracts quantity regardless of layout style
        quantity = details[1] if isinstance(details, list) else details.get("quantity", 0)
        if item not in prod or prod[item]["quantity"] < quantity:
            unavailable_items.append(item)
            
    if unavailable_items:
        return False, f"Checkout failed. The following items went out of stock or have insufficient inventory: {', '.join(unavailable_items)}. Please adjust your cart."
            
    for item, details in cart.items():
        # Safely extracts price and quantity regardless of layout style
        price = details[0] if isinstance(details, list) else details.get("price", 0.0)
        quantity = details[1] if isinstance(details, list) else details.get("quantity", 0)
        
        total += price * quantity
        prod[item]["quantity"] -= quantity
        items_list.append({"item": item, "price": price, "qty": quantity})
        
    order_id = str(uuid.uuid4())[:8].upper()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    order = {
        "id": order_id,
        "timestamp": timestamp,
        "items": items_list,
        "total": total
    }
    
    if "orders" not in data:
        data["orders"] = []
        
    data["orders"].insert(0, order)
    data["cart"] = {}
    
    database.save_data(data)
    return True, "Checkout successful"
def search_and_filter_products(query_name=None, min_price=None, max_price=None, category=None):
    from admin import database # Local import to fetch the database loader safely
    data = database.load_data()
    products = data.get("products", {})
    
    results = {}
    
    for item, details in products.items():
        # 1. Standardize item structure for handling both legacy list & dictionary schemas
        # Fix: Extract dictionary items using explicit keys instead of index numbers
        # Fix: Extract dictionary items using explicit keys instead of index numbers
        if isinstance(details, dict):
            price = details.get("price", 0.0)
            quantity = details.get("quantity", 0)
<<<<<<< HEAD
=======
            item_category = details.get("category", "Other")
            
>>>>>>> upstream/main
# Fallback to 'Other' if the category index is empty or missing
            item_category = details.get("category", "Other")
        elif isinstance(details, list):
            price = details[0] if len(details) > 0 else 0.0
            quantity = details[1] if len(details) > 1 else 0
            item_category = details[2] if len(details) > 2 else "Other"
        else:
            continue

        # 2. Guard: Substring Name Match
        if query_name and query_name.lower() not in item.lower():
            continue
            
        # 3. Guard: Minimum Price Filter
        if min_price is not None and price < min_price:
            continue
            
        # 4. Guard: Maximum Price Filter
        if max_price is not None and price > max_price:
            continue
            
        # 5. Guard: Category Match (Case-insensitive)
        if category and category.lower() != item_category.lower():
            continue
            
        # If the product survives all filter criteria guards, add it to results
        results[item] = {
            "price": price,
            "quantity": quantity,
            "category": item_category
        }
        
    return results