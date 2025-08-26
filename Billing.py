import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF

DB_PATH = "restaurant.db"

# ---------------- Database Functions ----------------
def save_order(customer_name, order_type, order_list, grand_total, payment_method):
    conn = sqlite3.connect(DB_PATH)
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

def fetch_orders(filter_type):
    conn = sqlite3.connect(DB_PATH)
    if filter_type == "Current Order":
        query = """
        SELECT * FROM orders
        WHERE DATE(order_datetime) = DATE('now', 'localtime')
        ORDER BY order_datetime DESC LIMIT 1
        """
    elif filter_type == "Daily":
        query = """
        SELECT * FROM orders
        WHERE DATE(order_datetime) = DATE('now', 'localtime')
        ORDER BY order_datetime DESC
        """
    elif filter_type == "Weekly":
        query = """
        SELECT * FROM orders
        WHERE DATE(order_datetime) >= DATE('now', '-7 days', 'localtime')
        ORDER BY order_datetime DESC
        """
    elif filter_type == "Monthly":
        query = """
        SELECT * FROM orders
        WHERE strftime('%Y-%m', order_datetime) = strftime('%Y-%m', 'now', 'localtime')
        ORDER BY order_datetime DESC
        """
    else:  # All Orders
        query = "SELECT * FROM orders ORDER BY order_datetime DESC"

    df = pd.read_sql_query(query, conn)
    conn.close()
    if not df.empty:
        df['order_datetime'] = pd.to_datetime(df['order_datetime']).dt.strftime("%d-%m-%Y %H:%M:%S")
    return df

# ---------------- PDF Export ----------------
def export_to_pdf(df, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    pdf.cell(200, 10, txt="Orders Report", ln=True, align="C")
    pdf.ln(5)

    col_width = pdf.w / (len(df.columns) + 1)
    for col in df.columns:
        pdf.cell(col_width, 10, col, border=1)
    pdf.ln()

    for _, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, 10, str(item), border=1)
        pdf.ln()

    pdf.output(filename)
    return filename

# ---------------- Streamlit UI ----------------
st.title("🍽 Restaurant Billing & Reports")

# ---------------- Billing Section ----------------
st.header("🧾 Billing System")

customer_name = st.text_input("Customer Name")
order_type = st.selectbox("Order Type", ["Dine-In", "Takeaway", "Delivery"])

menu_items = {"Burger": 100, "Pizza": 200, "Pasta": 150, "Coffee": 80}
order_list = []

st.subheader("Menu")
for item, price in menu_items.items():
    qty = st.number_input(f"{item} (₹{price})", min_value=0, step=1, key=item)
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

# ---------------- Reports Section ----------------
st.header("📋 Orders Report")

report_choice = st.selectbox("Select Report Type", ["Current Order", "Daily", "Weekly", "Monthly", "All Orders"])

df_orders = fetch_orders(report_choice)

if df_orders.empty:
    st.warning("No orders found for this selection.")
else:
    st.dataframe(df_orders)

    csv_data = df_orders.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download CSV",
        data=csv_data,
        file_name=f"{report_choice}_Orders.csv",
        mime="text/csv"
    )

    pdf_file = export_to_pdf(df_orders, f"{report_choice}_Orders.pdf")
    with open(pdf_file, "rb") as pdf:
        st.download_button(
            label="⬇ Download PDF",
            data=pdf,
            file_name=f"{report_choice}_Orders.pdf",
            mime="application/pdf"
        )
