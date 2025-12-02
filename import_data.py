import pandas as pd
import sqlite3

# Database path
db_path = r"C:\Users\ritik\Desktop\BankSight_App\banksight.db"

# CSV and JSON paths tumne diye hain, wo yahan daal dena
paths = {
    'Customers': r'C:\Users\ritik\Desktop\BankSight_App\customers.csv',
    'Accounts': r'C:\Users\ritik\Desktop\BankSight_App\accounts.csv',
    'Transactions': r'C:\Users\ritik\Desktop\BankSight_App\transactions.csv',
    'Loans_CSV': r'C:\Users\ritik\Desktop\BankSight_App\loans.csv',
    'CreditCards_JSON': r'C:\Users\ritik\Desktop\BankSight_App\credit_cards.json',
    'Branches_CSV': r'C:\Users\ritik\Desktop\BankSight_App\branches.csv',
    'SupportTickets_CSV': r'C:\Users\ritik\Desktop\BankSight_App\support_tickets.csv'
}

def load_csv_to_db(path, tablename):
    df = pd.read_csv(path)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(tablename, conn, if_exists='replace', index=False)
    print(f"{tablename} loaded.")

def load_json_to_db(path, tablename):
    import json
    with open(path, 'r') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(tablename, conn, if_exists='replace', index=False)
    print(f"{tablename} loaded.")

# Loading CSV tables
load_csv_to_db(paths['Customers'], 'Customers')
load_csv_to_db(paths['Accounts'], 'Accounts')
load_csv_to_db(paths['Transactions'], 'Transactions')
load_csv_to_db(paths['Loans_CSV'], 'Loans')
load_csv_to_db(paths['Branches_CSV'], 'Branches')
load_csv_to_db(paths['SupportTickets_CSV'], 'SupportTickets')

# Loading JSON tables
load_json_to_db(paths['CreditCards_JSON'], 'CreditCards')

print("All tables loaded into SQLite database.")
