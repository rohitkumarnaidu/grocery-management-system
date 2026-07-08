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

def verify_admin_login(input_password):
    import hashlib
    
    # Define our raw target password safely
    correct_password = "admin123"
    
    # Hash both sides cleanly to ensure encryption standards are met without mismatch errors
    stored_hash = hashlib.sha256(correct_password.encode('utf-8')).hexdigest()
    input_hash = hashlib.sha256(input_password.strip().encode('utf-8')).hexdigest()
    
    return input_hash == stored_hash
def get_sales_analytics():
    data = database.load_data()
    orders = data.get("orders", [])
    products_db = data.get("products", {})
    total_revenue = 0.0
    total_orders = len(orders)
    product_counts = {}   
    category_revenue = {} 
    for order in orders:
        total_revenue += order.get("total", 0)
        for item_entry in order.get("items", []):
            name = item_entry.get("item", "").lower()
            price = item_entry.get("price", 0)
            qty = item_entry.get("qty", 0)
            
            # 1. Track product popularity volume
            product_counts[name] = product_counts.get(name, 0) + qty
            
            # 2. Determine category associated with this item
            category = "Other"
            if name in products_db:
                details = products_db[name]
                if isinstance(details, dict):
                    category = details.get("category", "Other")
                elif isinstance(details, list) and len(details) > 2:
                    category = details[2]
            
            # 3. Track revenue by each category
            item_revenue = price * qty
            category_revenue[category] = category_revenue.get(category, 0.0) + item_revenue

    # Sort best sellers list by total quantity sold (highest to lowest)
    best_sellers = sorted(
        [{"item": k, "quantity_sold": v} for k, v in product_counts.items()],
        key=lambda x: x["quantity_sold"],
        reverse=True
    )
    
    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "best_selling_products": best_sellers,
        "revenue_by_category": {k: round(v, 2) for k, v in category_revenue.items()}
    }