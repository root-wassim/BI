import pandas as pd
import os
from db_connector import get_sql_engine, get_access_connection
from config import RAW_DIR

# Ensure raw folder exists
os.makedirs(RAW_DIR, exist_ok=True)

# Tables to extract (The roadmap mentions these)
TABLES = ['Orders', 'Customers', 'Employees', 'Order Details','shippers','Territories', 'EmployeeTerritories','Region' ]

def extract_from_sql_server():
    engine = get_sql_engine()
    if not engine:
        return

    for table in TABLES:
        try:
            query_table = f"[{table}]" if " " in table else table
            df = pd.read_sql(f"SELECT * FROM {query_table}", engine)
            
            # Save as sql_<tablename>.csv
            file_name = f"sql_{table.replace(' ', '_').lower()}.csv"
            output_path = os.path.join(RAW_DIR, file_name)
            
            df.to_csv(output_path, index=False)
            print(f" SQL Server: {table} -> {file_name} ({df.shape[0]} rows)")
        except Exception as e:
            print(f" SQL Server Error ({table}): {e}")

def extract_from_access():
    conn = get_access_connection()
    if not conn:
        return

    for table in TABLES:
        try:
            # Access queries don't always need brackets, but safe to use them
            query_table = f"[{table}]"
            query = f"SELECT * FROM {query_table}"
            
            df = pd.read_sql(query, conn)
            
            # Save as access_<tablename>.csv
            file_name = f"access_{table.replace(' ', '_').lower()}.csv"
            output_path = os.path.join(RAW_DIR, file_name)
            
            df.to_csv(output_path, index=False)
            print(f"Access:     {table} -> {file_name} ({df.shape[0]} rows)")
        except Exception as e:
            print(f" Access Error ({table}): {e}")
    
    conn.close()

if __name__ == "__main__":
    extract_from_sql_server()
    extract_from_access()
    print("\n Extraction Complete!")