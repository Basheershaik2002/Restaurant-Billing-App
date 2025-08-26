import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from fpdf import FPDF

DB_PATH = "restaurant.db"

# PDF export function
def export_to_pdf(df, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="Orders Report", ln=True, align="C")
    pdf.ln(5)

    # Table headers
    col_width = pdf.w / (len(df.columns) + 1)
    for col in df.columns:
        pdf.cell(col_width, 10, col, border=1)
    pdf.ln()

    # Table rows
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, 10, str(item), border=1)
        pdf.ln()

    pdf.output(filename)
    return filename

# Fetch orders with filters
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
    elif filter_type == "All Orders":
        query = """
        SELECT * FROM orders ORDER BY order_datetime DESC
        """
    else:
        conn.close()
        return pd.DataFrame()

    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        df['order_datetime'] = pd.to_datetime(df['order_datetime']).dt.strftime("%d-%m-%Y %H:%M:%S")
    return df

# Streamlit UI
st.title("📋 Orders Report")

report_choice = st.selectbox(
    "Select Report Type",
    ["Current Order", "Daily", "Weekly", "Monthly", "All Orders"]
)

df_orders = fetch_orders(report_choice)

if df_orders.empty:
    st.warning("No orders found for this selection.")
else:
    st.dataframe(df_orders)

    # CSV Download
    csv_data = df_orders.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download CSV",
        data=csv_data,
        file_name=f"{report_choice}_Orders.csv",
        mime="text/csv"
    )

    # PDF Download
    pdf_file = export_to_pdf(df_orders, f"{report_choice}_Orders.pdf")
    with open(pdf_file, "rb") as pdf:
        st.download_button(
            label="⬇ Download PDF",
            data=pdf,
            file_name=f"{report_choice}_Orders.pdf",
            mime="application/pdf"
        )
