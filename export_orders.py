# export_orders.py
import sqlite3
import pandas as pd

DB_FILE = "restaurant.db"
EXPORT_FILE = "orders_export.csv"

def export_orders():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM orders ORDER BY order_date DESC", conn)
    conn.close()

    if not df.empty:
        df.to_csv(EXPORT_FILE, index=False)
        print(f"✅ Orders exported successfully to {EXPORT_FILE}")
    else:
        print("⚠ No orders found to export.")

if __name__ == "__main__":
    export_orders()
