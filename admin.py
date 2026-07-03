import database

def get_inventory():
    data = database.load_data()
    return data.get("prod", {})

def add_prod(item, price, qty, category="Other"):
    data = database.load_data()
    item = item.lower()
    if "prod" not in data:
        data["prod"] = {}
    if item not in data["prod"]:
        data["prod"][item] = [price, qty, category]
        database.save_data(data)
        return True, "Item added successfully!"
    return False, "Item already exists"

def update_price(item, price):
    data = database.load_data()
    item = item.lower()
    if item in data.get("prod", {}):
        data["prod"][item][0] = price
        database.save_data(data)
        return True, "Price updated successfully!"
    return False, "Product does not exist"

def update_qty(item, qty):
    data = database.load_data()
    item = item.lower()
    if item in data.get("prod", {}):
        data["prod"][item][1] = qty
        database.save_data(data)
        return True, "Quantity updated successfully!"
    return False, "Product does not exist"

def delete_item(item):
    data = database.load_data()
    item = item.lower()
    if item in data.get("prod", {}):
        del data["prod"][item]
        # Also remove from cart if it exists
        if "cart" in data and item in data["cart"]:
            del data["cart"][item]
        database.save_data(data)
        return True, "Deleted successfully!"
    return False, "Product does not exist"
