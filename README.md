# Restaurant-Billing-App

Restaurant Billing & Reporting System

This is a project I built to simplify restaurant billing and make reporting seamless. The idea came from noticing how small restaurants often struggle with complicated POS systems that are either too expensive or too technical to manage.

I wanted to create a lightweight, simple-to-use tool that helps both staff (easy billing) and owners (clear reports) without adding unnecessary complexity.

You Can click the link to view sample app
(https://drive.google.com/file/d/1CDdCk-IA3fw6W3fCL3j7A_QjzcgGqpMf/view?usp=sharing)


Features

Billing System

Add customer details and select order type (Dine-In, Takeaway, Delivery)

Menu items with quantity selection and automatic price calculation

Subtotal, GST (5%), and Grand Total computed instantly

Multiple payment methods (Cash, Card, UPI)

All orders stored securely in an SQLite database


Reports Dashboard

View orders by Current Order, Daily, Weekly, Monthly, or All Orders

Export reports to CSV and PDF for easy sharing

Clean tabular view for better analysis



Tech Stack

Streamlit – for the user-friendly UI

SQLite – for storing order data

Pandas – for managing and displaying reports

FPDF – for exporting PDF reports

Python – the backbone of the project



Why I Built This

I’ve always been curious about building solutions that have real-world use cases. Restaurants are one of the places where speed, accuracy, and clarity matter a lot. By building this project, I challenged myself to design something that is both practical and impactful.

This isn’t just another coding exercise – it’s about solving a real problem:
Keeping billing simple while giving businesses the reports they need to grow.

 How to Run


Clone the repo:

git clone https://github.com/your-username/restaurant-billing.git
cd restaurant-billing


Install dependencies:

pip install -r requirements.txt



Run the app:

streamlit run Billing.py



Open http://localhost:8501 in your browser

This project is very close to me because it reflects how technology can make daily tasks easier. It’s a small step toward combining functionality and simplicity.
