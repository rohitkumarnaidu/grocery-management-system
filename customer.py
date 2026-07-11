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
        
    data["orders"].insert(0, order)
    data["cart"] = {}
    
    database.save_data(data)
    return True, f"Checkout successful! Total: Rs.{order['total']} (Saved Rs.{discount_amount})"   
    database.save_data(data)
    return True, "Checkout successful"
def search_and_filter_products(query_name=None, min_price=None, max_price=None, category=None):
    from admin import database 
    data = database.load_data()
    products = data.get("products", {})
    
    results = {}
    
    for item, details in products.items():
        if isinstance(details, dict):
            price = details.get("price", 0.0)
            quantity = details.get("quantity", 0)
            item_category = details.get("category", "Other")
        elif isinstance(details, list):
            price = details[0] if len(details) > 0 else 0.0
            quantity = details[1] if len(details) > 1 else 0
            item_category = details[2] if len(details) > 2 else "Other"
        else:
            continue
        if query_name and query_name.lower() not in item.lower():
            continue

def validate_coupon(code, cart_total):
    """
    Validates a coupon code against a given cart total.
    Returns (is_valid, discount_amount_or_error_message)
    """
    from admin import database  # Local import to prevent circular dependency
    data = database.load_data()
    coupons = data.get("coupons", {})
    code_upper = code.strip().upper()
    
    if code_upper not in coupons:
        return False, "Invalid coupon code"
        
    coupon = coupons[code_upper]
    if cart_total < coupon["min_purchase"]:
        return False, f"Minimum purchase amount of Rs.{coupon['min_purchase']} required for this coupon."
        
    if coupon["type"] == "percentage":
        discount = cart_total * (coupon["value"] / 100.0)
    elif coupon["type"] == "flat":
        discount = coupon["value"]
    else:
        return False, "Unknown coupon type structure"
        
    # Cap discount at total price so it doesn't go negative
    discount = min(discount, cart_total)
    return True, round(discount, 2)