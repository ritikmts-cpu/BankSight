🏦 BankSight – Banking Analytics & Credit/Debit Simulation
A comprehensive banking data analytics project simulating real-world accounts, customers, and transactions using Python, SQLite, and Streamlit.​

📌 Project Overview
This project uses a structured SQLite database (banksight.db) with multiple banking-related tables such as customers, accounts, and transactions.​
Data ko Streamlit dashboard ke through visualize, explore aur simulate kiya jata hai – including credit/debit operations, balance checks, and table exploration.​

🔧 Tech Stack
Python (pandas, sqlite3)​

Streamlit (interactive web dashboard)​

SQLite3 (banksight.db as local database)​

VS Code / any IDE

📂 Project Structure
📁 BankSight_App/
│
├── app.py → Main Streamlit application (all pages + simulation)​
├── banksight.db → SQLite database with banking tables​
│
├── 📁 data/ (optional)
│ └── CSVs used to create/populate tables
│
├── README.md
└── requirements.txt

🧹 Data & Database Summary
Multiple tables created in banksight.db for customers, accounts, and transactions.​

Data imported/cleaned from CSVs into SQLite using Python scripts (basic transformations & type cleaning).​

Proper primary keys & foreign key–style relations maintained for realistic banking flows.​

📊 Features & Analysis (Streamlit)
Home / Introduction

Project overview, objective, and short description of BankSight dashboard.​

View Tables Page

Dropdown se koi bhi table select karke uska data Streamlit me preview kar sakte ho.​

Large tables ke liye limited rows / optimized loading to avoid freezing.​

💰 Credit / Debit Simulation Page

User account/customer ID input karta hai, amount enter karta hai, aur action choose karta hai: Check Balance, Deposit, Withdraw.​

Current balance SQLite se fetch hota hai, business logic apply hota hai (insufficient balance check, etc.), aur phir updated balance database me commit hota hai.​

Clear success/error messages + updated balance display for realistic banking feel.​

🖥️ Dashboard Highlights
Includes:

Customer & account overview section.​

Table-wise data exploration for customers, accounts, transactions, etc.​

Interactive form-based credit/debit simulation with real-time balance update.​

🗄️ SQLite Operations
Safe read & write operations using sqlite3.connect() with proper commit and error-handling blocks.​

Functions to:

Fetch account/customer balance

Update balance after deposit/withdraw

Log or verify operations via database tables

📦 Installation
------------------------------
pip install -r requirements.txt
-------------------------------
----------------------------------
pip install streamlit pandas
-----------------------------------

🚀 How to Run
--------------------------------------
cd C:\Users\ritik\Desktop\BankSight_App
streamlit run app.py
-----------------------------------------
