import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ========================= PAGE CONFIG =========================
st.set_page_config(page_title="BankSight Dashboard", layout="wide")

# ========================= SQLITE CONNECTION =========================
@st.cache_resource
def get_connection():
    conn = sqlite3.connect("banksight.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=None):
    try:
        conn = get_connection()
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        return str(e)

def execute_non_select(query, params=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
        return True
    except Exception as e:
        return str(e)

# ========================= SIDEBAR NAVIGATION =========================
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Introduction",
        "📊 View Tables",
        "🔍 Filter Data",
        "✏️ CRUD Operations",
        "💰 Credit / Debit Simulation",
        "🧠 Analytical Insights",
        "👩‍💻 About Creator"
    ]
)

# ========================= INTRO PAGE =========================
if page == "🏠 Introduction":
    st.markdown("<h1 style='text-align:center;'>🏦 BankSight: Transaction Intelligence Dashboard</h1>", unsafe_allow_html=True)
    st.subheader("📌 Project Overview")
    st.write("""
    BankSight is a mini banking analytics platform designed to organize, analyze,
    and visualize core banking datasets.
    **This project is built using:**
    - Python  
    - SQLite3  
    - Streamlit  
    """)
    st.subheader("🎯 Project Objectives")
    st.write("""
    - Build an intuitive platform to explore banking datasets  
    - Enable quick table viewing using SQLite database  
    - Create a clean UI using Streamlit  
    - Improve visibility into accounts, customers, loans, and transactions  
    - Prepare base for filtering, CRUD, insights & simulations  
    """)
    st.write("---")
    st.success("Use the left navigation menu to explore the dashboard.")

# ========================= VIEW TABLES =========================
elif page == "📊 View Tables":
    st.header("📊 View Database Tables")
    tables = ["customers","accounts","transactions","branches","loans","support_tickets","credit_cards"]
    selected_table = st.selectbox("Select a table to view:", tables)
    if st.button("Load Table"):
        data = execute_query(f"SELECT * FROM {selected_table} LIMIT 2000")
        if isinstance(data, pd.DataFrame):
            st.dataframe(data, use_container_width=True)
        else:
            st.error("Error loading table: " + data)

# ========================= FILTER DATA =========================
elif page == "🔍 Filter Data":
    st.header("🔍 Filter Data")
    tables = ["customers","accounts","transactions","loans","credit_cards","branches","support_tickets"]
    selected_table = st.selectbox("Select Table to Filter", tables)
    if selected_table:
        df = execute_query(f"SELECT * FROM {selected_table}")
        st.subheader("Select columns and values to filter:")
        filters = {}
        for col in df.columns:
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) > 50:
                val = st.text_input(f"{col}:")
                if val.strip() != "":
                    filters[col] = val
            else:
                val = st.selectbox(f"{col}:", ["(No Filter)"] + list(unique_vals))
                if val != "(No Filter)":
                    filters[col] = val
        query = f"SELECT * FROM {selected_table}"
        if filters:
            conditions = [f"{col} = '{val}'" for col,val in filters.items()]
            query += " WHERE " + " AND ".join(conditions)
        result = execute_query(query)
        st.dataframe(result, use_container_width=True)

# ========================= CRUD OPERATIONS =========================
elif page == "✏️ CRUD Operations":
    st.header("✏️ CRUD Operations")
    tables_df = execute_query("SELECT name FROM sqlite_master WHERE type='table'")
    tables = tables_df['name'].tolist()
    selected_table = st.selectbox("Select a Table", tables)
    if selected_table:
        st.subheader("Select an Operation")
        operation = st.radio("Choose Operation", ["View","Add","Update","Delete"], horizontal=True)
        df = execute_query(f"SELECT * FROM {selected_table}")
        if df.empty:
            st.warning("This table is empty!")
        else:
            if operation=="View":
                st.dataframe(df,use_container_width=True)
            elif operation=="Add":
                new_data={}
                for col in df.columns:
                    new_data[col]=st.text_input(f"Enter {col}")
                if st.button("Add Record"):
                    cols = ", ".join(df.columns)
                    placeholders = ", ".join(["?"]*len(df.columns))
                    query = f"INSERT INTO {selected_table} ({cols}) VALUES ({placeholders})"
                    execute_non_select(query, tuple(new_data.values()))
                    st.success("Record added!")
                    
            elif operation=="Update":
                unique_col = df.columns[0]
                picked_id = st.selectbox(f"Select {unique_col} to update", df[unique_col].unique().tolist())
                selected_row = df[df[unique_col]==picked_id].iloc[0]
                updated_data = {}
                for col in df.columns:
                    updated_data[col]=st.text_input(col,str(selected_row[col]))
                if st.button("Update Record"):
                    set_clause = ", ".join([f"{col} = ?" for col in updated_data])
                    query = f"UPDATE {selected_table} SET {set_clause} WHERE {unique_col} = ?"
                    execute_non_select(query, tuple(updated_data.values())+(picked_id,))
                    st.success("Record updated!")
                    
            elif operation=="Delete":
                unique_col = df.columns[0]
                picked_id = st.selectbox(f"Select {unique_col} to delete", df[unique_col].unique().tolist())
                confirm = st.checkbox("Are you sure?")
                if st.button("Delete Record") and confirm:
                    query=f"DELETE FROM {selected_table} WHERE {unique_col}=?"
                    execute_non_select(query,(picked_id,))
                    st.error("Record deleted!")
                    

# ========================= CREDIT/DEBIT SIMULATION =========================
# ========================= CREDIT/DEBIT SIMULATION =========================
elif page=="💰 Credit / Debit Simulation":
    st.header("💰 Credit / Debit Simulation")
    customer_id = st.text_input("Enter Account ID:")
    amount = st.number_input("Enter Amount (₹):", min_value=0.0, step=1.0, format="%.2f")
    action = st.radio("Select Action", ["Check Balance","Deposit","Withdraw"])
    submit_btn = st.button("Submit")
    
    DB_PATH = "banksight.db"
    
    def fetch_balance(cust_id):
        try:
            # ✅ String ke tarah rakho, int() mat karo
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query(
                "SELECT account_balance FROM accounts WHERE customer_id=?",
                con=conn,
                params=(cust_id,)
            )
            conn.close()
            if not df.empty:
                return df.at[0, "account_balance"]
            return None
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return None
    
    def update_balance(cust_id, new_balance):
        try:
            # ✅ String ke tarah rakho
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "UPDATE accounts SET account_balance=?, last_updated=? WHERE customer_id=?",
                (new_balance, now, cust_id)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    if submit_btn:
        if not customer_id.strip():
            st.warning("Please enter a valid Account ID.")
        else:
            balance = fetch_balance(customer_id)
            if balance is None:
                st.error("❌ Account ID not found.")
            else:
                if action == "Check Balance":
                    st.info(f"💰 Current Balance: ₹{balance:,.2f}")
                elif action == "Deposit":
                    new_balance = balance + amount
                    update_balance(customer_id, new_balance)
                    st.success(f"✅ ₹{amount:,.2f} deposited! 💰 New Balance: ₹{new_balance:,.2f}")
                elif action == "Withdraw":
                    if balance - amount < 1000:
                        st.error("❌ Transaction denied: Minimum balance ₹1000 must be maintained.")
                        st.info(f"💰 Current Balance: ₹{balance:,.2f}")
                    else:
                        new_balance = balance - amount
                        update_balance(customer_id, new_balance)
                        st.success(f"✅ ₹{amount:,.2f} withdrawn! 💰 New Balance: ₹{new_balance:,.2f}")


# ========================= ANALYTICAL INSIGHTS =========================
elif page=="🧠 Analytical Insights":
    st.header("🧠 Analytical Insights")
    st.markdown("""
Select a question from the dropdown. The query executes live on the SQLite database.  
Results are shown in a table with SQL query for transparency.
""")
    questions = {
        "Q1: How many customers exist per city, and what is their average account balance?": """
            SELECT c.city, COUNT(*) AS total_customers, AVG(a.account_balance) AS average_balance
            FROM Customers c
            JOIN Accounts a ON c.customer_id = a.customer_id
            GROUP BY c.city;
        """,
        "Q2: Which account type (Savings, Current, Loan, etc.) holds the highest total balance?": """
            SELECT account_type, SUM(balance) AS total_balance
            FROM (
                SELECT 'Savings/Current' AS account_type, account_balance AS balance
                FROM Accounts
                WHERE account_type IN ('Savings','Current')
                UNION ALL
                SELECT 'Loan' AS account_type, Loan_Amount AS balance
                FROM Loans
            )
            GROUP BY account_type
            ORDER BY total_balance DESC
            LIMIT 1;
        """,
        "Q3: Who are the top 10 customers by total account balance across all account types?": """
            SELECT c.customer_id, c.name, SUM(a.account_balance) AS total_balance
            FROM Customers c
            JOIN Accounts a ON c.customer_id = a.customer_id
            GROUP BY c.customer_id, c.name
            ORDER BY total_balance DESC
            LIMIT 10;
        """,
        "Q4: Which customers opened accounts in 2023 with a balance above ₹1,00,000?": """
            SELECT c.customer_id, c.name, a.account_balance, c.join_date
            FROM Customers c
            JOIN Accounts a ON c.customer_id = a.customer_id
            WHERE strftime('%Y', c.join_date) = '2023'
              AND a.account_balance > 100000;
        """,
        "Q5: What is the total transaction volume (sum of amounts) by transaction type?": """
            SELECT txn_type, SUM(amount) AS total_transaction_volume
            FROM Transactions
            GROUP BY txn_type
            ORDER BY total_transaction_volume DESC;
        """,
        "Q6: Which accounts have more than 3 failed transactions in a single month?": """
            SELECT customer_id, strftime('%Y-%m', txn_time) AS year_month, COUNT(*) AS failed_count
            FROM Transactions
            WHERE status='failed'
            GROUP BY customer_id, year_month
            HAVING COUNT(*)>3;
        """,
        "Q7: Which are the top 5 branches by total transaction volume in the last 6 months?": """
            SELECT b.Branch_Name, SUM(t.amount) AS total_transaction_volume
            FROM Transactions t
            JOIN Customers c ON t.customer_id=c.customer_id
            JOIN Branches b ON c.city=b.City
            WHERE t.txn_time >= date('now','-6 months')
            GROUP BY b.Branch_Name
            ORDER BY total_transaction_volume DESC
            LIMIT 5;
        """,
        "Q8: Which accounts have 5 or more high-value transactions above ₹2,00,000?": """
            SELECT customer_id, COUNT(*) AS high_value_txn_count
            FROM Transactions
            WHERE amount>200000
            GROUP BY customer_id
            HAVING COUNT(*)>=5;
        """,
        "Q9: What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?": """
            SELECT Loan_Type, AVG(Loan_Amount) AS avg_loan, AVG(Interest_Rate) AS avg_interest_rate
            FROM Loans
            GROUP BY Loan_Type;
        """,
        "Q10: Which customers currently hold more than one active or approved loan?": """
            SELECT Customer_ID, COUNT(*) AS loan_count
            FROM Loans
            WHERE Loan_Status IN ('Active','Approved')
            GROUP BY Customer_ID
            HAVING COUNT(*)>1;
        """,
        "Q11: Who are the top 5 customers with the highest outstanding (non-closed) loan amounts?": """
            SELECT Customer_ID, SUM(Loan_Amount) AS total_outstanding
            FROM Loans
            WHERE Loan_Status != 'Closed'
            GROUP BY Customer_ID
            ORDER BY total_outstanding DESC
            LIMIT 5;
        """,
        "Q12: Which branch holds the highest total account balance?": """
            SELECT b.Branch_Name, SUM(a.account_balance) AS total_account_balance
            FROM Accounts a
            JOIN Customers c ON a.customer_id=c.customer_id
            JOIN Branches b ON c.city=b.City
            GROUP BY b.Branch_Name
            ORDER BY total_account_balance DESC
            LIMIT 1;
        """,
        "Q13: What is the branch performance summary showing total customers, total loans, and transaction volume?": """
            SELECT b.Branch_Name,
                   COUNT(DISTINCT c.customer_id) AS total_customers,
                   COUNT(DISTINCT l.Loan_ID) AS total_loans,
                   SUM(t.amount) AS total_transaction_volume
            FROM Branches b
            LEFT JOIN Customers c ON b.City=c.City
            LEFT JOIN Loans l ON c.customer_id=l.Customer_ID
            LEFT JOIN Transactions t ON c.customer_id=t.customer_id
            GROUP BY b.Branch_Name
            ORDER BY b.Branch_Name;
        """,
        "Q14: Which issue categories have the longest average resolution time?": """
            SELECT Issue_Category,
                   AVG(julianday(Date_Closed)-julianday(Date_Opened)) AS avg_resolution_days
            FROM Support_Tickets
            WHERE Date_Closed IS NOT NULL
            GROUP BY Issue_Category
            ORDER BY avg_resolution_days DESC;
        """,
        "Q15: Which support agents have resolved the most critical tickets with high customer ratings (≥4)?": """
            SELECT Support_Agent,
                   COUNT(*) AS resolved_critical_high_rating_tickets
            FROM Support_Tickets
            WHERE Priority='Critical' AND Customer_Rating>=4 AND Status IN ('Resolved','Closed')
            GROUP BY Support_Agent
            ORDER BY resolved_critical_high_rating_tickets DESC;
        """
    }

    selected_question = st.selectbox("Select a Question", list(questions.keys()))
    if st.button("Run Query"):
        query = questions[selected_question]
        df_result = execute_query(query)
        st.markdown("**Executed SQL Query:**")
        st.code(query)
        if isinstance(df_result, pd.DataFrame):
            st.dataframe(df_result)
        else:
            st.error(f"Error executing query: {df_result}")


# ========================= ABOUT CREATOR =========================
elif page == "👩‍💻 About Creator":
    st.header("👩‍💻 About Creator")

    st.write("**Name:** Ritik")  
    st.write("**Email:** ritik@example.com") 
    st.write("**Phone:** 7494963205")  
    st.write("**GitHub:** [ritikmts-cpu](https://github.com/ritikmts-cpu)")

    st.write("---")
    st.write("""
I am the creator of this BankSight Dashboard, designed to provide insights into banking datasets,
perform CRUD operations, simulate account transactions, and explore analytical queries.

This project demonstrates Python, SQLite, and Streamlit integration for a real-world mini banking analytics platform.
""")
    st.success("Thank you for exploring the BankSight Dashboard!")