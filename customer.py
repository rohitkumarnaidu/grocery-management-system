import database
import time
import uuid

def get_cart():
    data = database.load_data()
    return data.get("cart", {})

def add_item(item, qty):
    data = database.load_data()
    item = item.lower()
    
    if item not in data.get("prod", {}):
        return False, "Product does not exist in inventory"
        
    price = data["prod"][item][0]
    
    if "cart" not in data:
        data["cart"] = {}
        
    if item in data["cart"]:
        data["cart"][item][1] += qty
    else:
        data["cart"][item] = [price, qty]
        
    database.save_data(data)
    return True, "Added to cart"

def delete_item(item):
    data = database.load_data()
    item = item.lower()
    if item in data.get("cart", {}):
        del data["cart"][item]
        database.save_data(data)
        return True, "Deleted from cart"
    return False, "Product not in cart"

def update_item_qty(item, qty):
    data = database.load_data()
    item = item.lower()
    if item in data.get("cart", {}):
        if qty <= 0:
            del data["cart"][item]
        else:
            data["cart"][item][1] = qty
        database.save_data(data)
        return True, "Cart updated"
    return False, "Product not in cart"

def view_tp():
    data = database.load_data()
    cart = data.get("cart", {})
    tp = sum(cart[item][0] * cart[item][1] for item in cart)
    return tp

def checkout():
    data = database.load_data()
    cart = data.get("cart", {})
    
    if not cart:
        return False, "Cart is empty"
        
    prod = data.get("prod", {})
    total = 0
    items_list = []
    
    # Check inventory first
    for item, details in cart.items():
        qty = details[1]
        if item not in prod or prod[item][1] < qty:
            return False, f"Not enough stock for {item}"
            
    # Process checkout
    for item, details in cart.items():
        price = details[0]
        qty = details[1]
        total += price * qty
        prod[item][1] -= qty
        items_list.append({"item": item, "price": price, "qty": qty})
        
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
        
    data["orders"].insert(0, order) # Add to top of list
    data["cart"] = {} # Empty the cart
    
    database.save_data(data)
    return True, "Checkout successful"
