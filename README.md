# Grocery Management System 🛒

A web-based grocery management system with a **React (Vite)** frontend and a **Python (Flask)** REST API backend. It supports two perspectives — **Admin** and **Customer** — for managing inventory, browsing products, and handling billing/checkout.

---

## Project Structure

```
grocery-management-system/
├── .vscode/            # Editor settings
├── frontend/           # React (Vite) frontend application
├── admin.py            # Admin-side logic (inventory management, product CRUD)
├── app.py              # Flask application entry point / API routes
├── customer.py         # Customer-side logic (browsing, cart, checkout)
├── database.py         # Data access layer for SQLite
├── grocery.db          # SQLite database file used for data persistence
├── migrate_json_to_sqlite.py # One-time data migration script from JSON to DB
├── requirements.txt    # Python backend dependencies
├── .gitignore
└── README.md
```

The backend and frontend are decoupled: the Flask API serves data over REST, and the React app consumes it as a separate client.

---

## Features

### 👨‍💼 Admin
- Add new products with name, price, quantity, and category
- Update the price or quantity of existing products
- Delete products from inventory
- Filter inventory by product category
- View the full order/transaction history

### 🛒 Customer
- Browse products by category
- Add items to a cart and adjust quantities
- Checkout — deducts inventory and logs the order
- View recent order history

---

## Tech Stack

- **Frontend**: React, Vite
- **Backend**: Python 3, Flask
- **Data Persistence**: SQLite database (`grocery.db`)

---

## Getting Started

Since the app is split into a backend and frontend, run each separately.

### 1. Backend (Flask API)

```bash
git clone https://github.com/vanshika114/grocery-management-system.git
cd grocery-management-system

# Create and activate a virtual environment
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Migrate existing JSON data to SQLite (run once if migrating from legacy data.json)
python migrate_json_to_sqlite.py

# Run the API
python app.py
```

The API runs on `http://127.0.0.1:5000` by default.

### 2. Frontend (React + Vite)

In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the local URL Vite prints in the terminal (usually `http://localhost:5173/`).

---

## Contributing

Issues and pull requests are welcome. Please open an issue first to discuss any significant change.

## License

No license specified yet — check with the repository owner before reuse.
