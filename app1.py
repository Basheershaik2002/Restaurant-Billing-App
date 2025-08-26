import streamlit as st
import sqlite3
from datetime import datetime

# Function to save order to DB
def save_order(customer_name, order_type, order_list, grand_total, payment_method):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    for item in order_list:
        item_name, price, quantity, total_price = item
        cursor.execute("""
            INSERT INTO orders 
            (customer_name, order_type, item_name, price, quantity, total_price, payment_method, order_datetime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_name,
            order_type,
            item_name,
            price,
            quantity,
            total_price,
            payment_method,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
    conn.commit()
    conn.close()

# --- Streamlit UI ---
st.title("Restaurant Billing System")

customer_name = st.text_input("Customer Name")
order_type = st.selectbox("Order Type", ["Dine-In", "Takeaway", "Delivery"])

menu_items = {
    "Burger": 100,
    "Pizza": 200,
    "Pasta": 150,
    "Coffee": 80
}

order_list = []
st.subheader("Menu")
for item, price in menu_items.items():
    qty = st.number_input(f"{item} (₹{price})", min_value=0, step=1)
    if qty > 0:
        order_list.append((item, price, qty, price * qty))

if order_list:
    st.subheader("Order Summary")
    subtotal = sum(item[3] for item in order_list)
    gst = subtotal * 0.05
    grand_total = subtotal + gst

    st.write(f"Subtotal: ₹{subtotal:.2f}")
    st.write(f"GST (5%): ₹{gst:.2f}")
    st.write(f"Total: ₹{grand_total:.2f}")

    payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI"])

    if st.button("Place Order"):
        save_order(customer_name, order_type, order_list, grand_total, payment_method)
        st.success(f"✅ Order placed successfully for {customer_name}!")

