import database
import time
import uuid

def get_cart():
    data = database.load_data()
    return data.get("cart", {})

def add_item(item, quantity):
    data = database.load_data()
    item = item.lower()
    
    # using 'products' in place of 'prod'
    if item not in data.get("products", {}):
        return False, "Product does not exist in inventory"
        
    price = data["products"][item][0]
    available_stock = data["products"][item][1]
    
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
    data = database.load_data()
    item = item.strip().lower()
    if item in data.get("cart", {}):
        if quantity <= 0:
            del data["cart"][item]
        else:
            data["cart"][item][1] = quantity
        database.save_data(data)
        return True, "Cart updated"
    return False, "Product not in cart"

def view_total_price():
    data = database.load_data()
    cart = data.get("cart", {})
    total_price = sum(cart[item][0] * cart[item][1] for item in cart)
    return total_price

def checkout():
    data = database.load_data()
    cart = data.get("cart", {})
    
    if not cart:
        return False, "Cart is empty"
        
    prod = data.get("products", {})
    total = 0
    items_list = []
    
    # CHECK IF ANY ITEM IN THE CART HAS GONE OUT OF STOCK BEFORE PROCESSING THE BILL
    unavailable_items = []
    for item, details in cart.items():
        quantity = details[1]
        if item not in prod or prod[item][1] < quantity:
            unavailable_items.append(item)
            
    if unavailable_items:
        return False, f"Checkout failed. The following items went out of stock or have insufficient inventory: {', '.join(unavailable_items)}. Please adjust your cart."
            
    # Check inventory first
    for item, details in cart.items():
        quantity = details[1]
        if item not in prod or prod[item][1] < quantity:
            return False, f"Not enough stock for {item}"
            
    # Process checkout
    for item, details in cart.items():
        price = details[0]
        quantity = details[1]
        total += price * quantity
        prod[item][1] -= quantity
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