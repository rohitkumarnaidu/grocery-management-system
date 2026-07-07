import database

def get_inventory():
    data = database.load_data()
    # using 'products' in place of 'prod'
    return data.get("products", {})

def add_product(item, price, quantity, category="Other"):
    data = database.load_data()
    item = item.lower()
    if "products" not in data:
        data["products"] = {}
    if item not in data["products"]:
        data["products"][item] = [price, quantity, category]
        database.save_data(data)
        return True, "Item added successfully!"
    return False, "Item already exists"

def update_price(item, price):
    data = database.load_data()
    item = item.lower()
    if item in data.get("products", {}):
        data["products"][item][0] = price
        database.save_data(data)
        return True, "Price updated successfully!"
    return False, "Product does not exist"

def update_quantity(item, quantity):
    data = database.load_data()
    item = item.lower()
    if item in data.get("products", {}):
        data["products"][item][1] = quantity
        database.save_data(data)
        return True, "Quantity updated successfully!"
    return False, "Product does not exist"

def delete_item(item):
    data = database.load_data()
    item = item.lower()
    if item in data.get("products", {}):
        del data["products"][item]
        # Also remove from cart if it exists
        if "cart" in data and item in data["cart"]:
            del data["cart"][item]
        database.save_data(data)
        return True, "Deleted successfully!"
    return False, "Product does not exist"

def get_low_stock_alerts(threshold=5):
    """
    Scans the inventory data and returns products that fall below the threshold.
    Handles both legacy list formats and new dictionary structures.
    """
    data = database.load_data()
    products = data.get("products", {})
    alerts = {}
    
    for item, details in products.items():
        # 1. Handle new dictionary format
        if isinstance(details, dict):
            quantity = details.get("quantity", 0)
            price = details.get("price", 0)
            category = details.get("category", "Other")
            
        # 2. Handle legacy list format securely
        elif isinstance(details, list):
            price = details[0] if len(details) > 0 else 0
            quantity = details[1] if len(details) > 1 else 0
            category = details[2] if len(details) > 2 else "Other"
            
        else:
            continue 
            
        # Evaluate against threshold
        if quantity < threshold:
            alerts[item] = {
                "price": price,
                "quantity": quantity,
                "category": category,
                "status": "Out of Stock" if quantity == 0 else "Low Stock"
            }
            
    return alerts