import sqlite3
import pandas as pd

# Connect to the database file Python just made
conn = sqlite3.connect("bluestock_mf.db")

print("--- RUNNING SAMPLE SQL QUERIES ---\n")

# Query 1: Top 5 Funds by AUM
query_1 = """
SELECT f.scheme_name, p.aum_crores 
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crores DESC 
LIMIT 5;
"""
print("🏆 TOP 5 FUNDS BY AUM SIZE:")
df1 = pd.read_sql_query(query_1, conn)
print(df1)
print("\n" + "="*50 + "\n")


# Query 2: Geographical Transaction Capital Inflows
query_2 = """
SELECT state, COUNT(transaction_id) as total_transactions, SUM(amount) as total_capital
FROM fact_transactions
GROUP BY state
ORDER BY total_capital DESC;
"""
print("📍 CAPITAL INFLOWS BY STATE:")
df2 = pd.read_sql_query(query_2, conn)
print(df2)
print("\n" + "="*50 + "\n")

conn.close()