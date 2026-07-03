import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"prod": {}, "cart": {}, "orders": []}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"prod": {}, "cart": {}, "orders": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
