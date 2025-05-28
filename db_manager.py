# database/db_manager.py - Database Management
import sqlite3
from datetime import datetime
import os


class DatabaseManager:
    def __init__(self, db_name="restaurant_payment.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.insert_sample_data()

    def connect(self):
        """Connect to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            # Enable foreign key support
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def create_tables(self):
        """Create all necessary tables"""
        try:
            # Menu items table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    description TEXT,
                    available BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Customers table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Payments table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    customer_name TEXT NOT NULL,
                    total_amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    payment_status TEXT DEFAULT 'Completed',
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            """)

            # Order items table (for detailed order tracking)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payment_id INTEGER NOT NULL,
                    menu_item_id INTEGER NOT NULL,
                    menu_item_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (payment_id) REFERENCES payments (id),
                    FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
                )
            """)

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def insert_sample_data(self):
        """Insert sample data if tables are empty"""
        try:
            # Check if menu items already exist
            self.cursor.execute("SELECT COUNT(*) FROM menu_items")
            if self.cursor.fetchone()[0] == 0:
                sample_menu = [
                    ("Nasi Gudeg", "Makanan Utama", 15000, "Nasi dengan gudeg khas Yogyakarta", 1),
                    ("Ayam Geprek", "Makanan Utama", 18000, "Ayam goreng geprek dengan sambal", 1),
                    ("Soto Ayam", "Makanan Utama", 12000, "Soto ayam dengan kuah bening", 1),
                    ("Gado-gado", "Makanan Utama", 10000, "Salad Indonesia dengan bumbu kacang", 1),
                    ("Es Teh Manis", "Minuman", 3000, "Teh manis dingin", 1),
                    ("Es Jeruk", "Minuman", 5000, "Jus jeruk segar", 1),
                    ("Kopi Hitam", "Minuman", 4000, "Kopi hitam panas", 1),
                    ("Kerupuk", "Tambahan", 2000, "Kerupuk renyah", 1),
                    ("Sambal Extra", "Tambahan", 1000, "Sambal pedas tambahan", 1)
                ]

                self.cursor.executemany("""
                    INSERT INTO menu_items (name, category, price, description, available)
                    VALUES (?, ?, ?, ?, ?)
                """, sample_menu)

            # Check if customers already exist
            self.cursor.execute("SELECT COUNT(*) FROM customers")
            if self.cursor.fetchone()[0] == 0:
                sample_customers = [
                    ("John Doe", "081234567890", "john@email.com", "Jl. Merdeka No. 1"),
                    ("Jane Smith", "081234567891", "jane@email.com", "Jl. Sudirman No. 2"),
                    ("Ahmad Rahman", "081234567892", "ahmad@email.com", "Jl. Thamrin No. 3"),
                    ("Siti Nurhaliza", "081234567893", "siti@email.com", "Jl. Gatot Subroto No. 4")
                ]

                self.cursor.executemany("""
                    INSERT INTO customers (name, phone, email, address)
                    VALUES (?, ?, ?, ?)
                """, sample_customers)

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting sample data: {e}")

    def get_menu_items(self):
        """Get all menu items"""
        try:
            self.cursor.execute("""
                SELECT id, name, category, price, description, available
                FROM menu_items
                ORDER BY category, name
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching menu items: {e}")
            return []

    def add_menu_item(self, name, category, price, description="", available=True):
        """Add new menu item"""
        try:
            self.cursor.execute("""
                INSERT INTO menu_items (name, category, price, description, available)
                VALUES (?, ?, ?, ?, ?)
            """, (name, category, price, description, available))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding menu item: {e}")
            return False

    def update_menu_item(self, item_id, name, category, price, description="", available=True):
        """Update menu item"""
        try:
            self.cursor.execute("""
                UPDATE menu_items
                SET name=?, category=?, price=?, description=?, available=?
                WHERE id=?
            """, (name, category, price, description, available, item_id))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating menu item: {e}")
            return False

    def delete_menu_item(self, item_id):
        """Delete menu item"""
        try:
            self.cursor.execute("DELETE FROM menu_items WHERE id=?", (item_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting menu item: {e}")
            return False

    def add_payment(self, customer_name, total_amount, payment_method, notes=""):
        """Add new payment record"""
        try:
            self.cursor.execute("""
                INSERT INTO payments (customer_name, total_amount, payment_method, notes)
                VALUES (?, ?, ?, ?)
            """, (customer_name, total_amount, payment_method, notes))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding payment: {e}")
            return None

    def get_payments(self):
        """Get all payment records"""
        try:
            self.cursor.execute("""
                SELECT id, customer_name, total_amount, payment_method, 
                       payment_status, order_date, notes
                FROM payments
                ORDER BY order_date DESC
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching payments: {e}")
            return []

    def update_payment(self, payment_id, customer_name, total_amount, payment_method, notes=""):
        """Update payment record"""
        try:
            self.cursor.execute("""
                UPDATE payments
                SET customer_name=?, total_amount=?, payment_method=?, notes=?
                WHERE id=?
            """, (customer_name, total_amount, payment_method, notes, payment_id))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating payment: {e}")
            return False

    def delete_payment(self, payment_id):
        """Delete payment record"""
        try:
            self.cursor.execute("DELETE FROM payments WHERE id=?", (payment_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting payment: {e}")
            return False

    def search_payments(self, search_term):
        """Search payments by customer name or ID"""
        try:
            self.cursor.execute("""
                SELECT id, customer_name, total_amount, payment_method, 
                       payment_status, order_date, notes
                FROM payments
                WHERE customer_name LIKE ? OR id LIKE ?
                ORDER BY order_date DESC
            """, (f"%{search_term}%", f"%{search_term}%"))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching payments: {e}")
            return []

    def search_menu_items(self, search_term):
        """Search menu items by name"""
        try:
            self.cursor.execute("""
                SELECT id, name, category, price, description, available
                FROM menu_items
                WHERE name LIKE ? OR category LIKE ?
                ORDER BY category, name
            """, (f"%{search_term}%", f"%{search_term}%"))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching menu items: {e}")
            return []

    def get_daily_report(self, date=None):
        """Get daily sales report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            self.cursor.execute("""
                SELECT COUNT(*) as total_transactions,
                       SUM(total_amount) as total_revenue,
                       AVG(total_amount) as avg_transaction
                FROM payments
                WHERE DATE(order_date) = ?
            """, (date,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting daily report: {e}")
            return (0, 0, 0)

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()