# Grocery Management System 🛒

A modern, visually stunning **Web-based Grocery Management System** built with **React (Vite + Shadcn UI)** for the frontend and **Python (Flask)** for the backend REST API.  
This project helps manage grocery items, inventory, and billing from two perspectives: **Admin** and **Customer**.

> **Note:** This project successfully resolves the following issues from the original repository:
> - **[#20: Migrate CLI to modern web GUI](https://github.com/vanshika114/grocery-management-system/issues/20)**
> - **[#17: Product categories](https://github.com/vanshika114/grocery-management-system/issues/17)**
> - **[#19: Order history for customers and admin](https://github.com/vanshika114/grocery-management-system/issues/19)**

---

## Features

### 👨‍💼 Admin Dashboard
1. Add new products with name, price, quantity, and category
2. Update the price or quantity of existing products inline
3. Delete products from inventory
4. Filter inventory by product category
5. View a **Global Order Ledger** with complete transaction history

### 🛒 Customer Shop
1. Browse products with a beautiful card-based layout
2. Filter products by category using interactive pill tabs
3. Add items to cart and adjust quantities
4. Checkout — automatically deducts inventory and logs the order
5. View **Recent Orders** with order ID, timestamp, items, and total

### 📦 Product Categories
Products are organized into 10 categories for easier browsing:
- 🥛 Dairy · 🧃 Beverages · 🍿 Snacks · 🥬 Fruits & Vegetables · 🌾 Grains & Cereals
- 🥖 Bakery · 🥩 Meat & Seafood · 🧊 Frozen Foods · 🏠 Household · 📦 Other

### 🧾 Order History
- Each order is saved with: **order ID**, **timestamp**, **items with quantities**, and **total**
- Customers can view their recent orders
- Admins can view all past orders in a structured table

---

## Technologies Used
- **Frontend**: React 19, Vite, Tailwind CSS 3, Shadcn UI, Lucide Icons
- **UI Design**: Premium light theme with glassmorphism, Inter font, violet accents, category emojis
- **Backend**: Python 3, Flask, Flask-CORS
- **Data Persistence**: JSON file (`data.json`)

---

## How to Run the Project

Since the application is built with a decoupled architecture, you need to run **two** separate servers: the Flask API and the React Development Server.

### 1. Start the Flask Backend API

1. Clone the repository:
   ```bash
   git clone https://github.com/Keshavsspppp/grocery-management-system.git
   cd grocery-management-system
   ```

2. Set up the Python virtual environment and install dependencies:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Mac/Linux
   source venv/bin/activate
   
   pip install Flask flask-cors
   ```

3. Run the Flask API server:
   ```bash
   python app.py
   ```
   *(The API will run on `http://127.0.0.1:5000`)*

---

### 2. Start the React Frontend

Open a **new terminal window/tab**:

1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to the local URL provided by Vite (usually `http://localhost:5173/`).

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products` | Get all products |
| `POST` | `/api/products` | Add a new product |
| `PUT` | `/api/products/<item>/price` | Update product price |
| `PUT` | `/api/products/<item>/qty` | Update product quantity |
| `DELETE` | `/api/products/<item>` | Delete a product |
| `GET` | `/api/cart` | Get cart contents & total |
| `POST` | `/api/cart` | Add item to cart |
| `PUT` | `/api/cart/<item>` | Update cart item qty |
| `DELETE` | `/api/cart/<item>` | Remove item from cart |
| `POST` | `/api/checkout` | Process checkout |
| `GET` | `/api/orders` | Get all past orders |
