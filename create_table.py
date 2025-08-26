import sqlite3

conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS orders")

cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    item_name TEXT,
    quantity INTEGER,
    price REAL,
    total REAL,
    payment_method TEXT,
    order_date TEXT
)
""")

conn.commit()
conn.close()

print("Orders table created successfully.")
