import sqlite3

conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in DB:", tables)

if ("menu",) in tables:
    cursor.execute("SELECT * FROM menu")
    rows = cursor.fetchall()
    print("\nMenu table contents:")
    for row in rows:
        print(row)
else:
    print("\n❌ Menu table does not exist!")

conn.close()
