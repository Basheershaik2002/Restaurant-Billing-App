import sqlite3
from datetime import datetime

DB_FILE = "restaurant.db"

# Sample data
sample_orders = [
    ("John Doe", datetime.now().strftime("%Y-%m-%d"), "Burger, Fries", 250.00, 12.50, 262.50),
    ("Alice Smith", datetime.now().strftime("%Y-%m-%d"), "Pizza, Coke", 300.00, 15.00, 315.00),
    ("David Johnson", datetime.now().strftime("%Y-%m-%d"), "Pasta, Garlic Bread", 350.00, 17.50, 367.50),
]

def insert_orders():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO orders (customer_name, order_date, items, subtotal, gst, total)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_orders)

    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(sample_orders)} sample orders into '{DB_FILE}'.")

if __name__ == "__main__":
    insert_orders()
