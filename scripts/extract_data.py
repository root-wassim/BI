import pandas as pd
import os
# We import the functions we just created in Step 1
from database_connect import get_sql_engine, get_access_connection
from config import RAW_DIR

# Ensure raw folder exists
os.makedirs(RAW_DIR, exist_ok=True)

# The EXACT list of tables from your friend's code
TABLES = ['Orders', 'Customers', 'Employees', 'Order Details','shippers','Territories', 'EmployeeTerritories','Region' ]

def extract_from_sql_server():
    engine = get_sql_engine()
    # If no SQL Server, we just return silently or print error if you prefer
    if not engine:
        # print(" [SQL Server] Connection failed.") 
        return

    for table in TABLES:
        try:
            query_table = f"[{table}]"
            df = pd.read_sql(f"SELECT * FROM {query_table}", engine)
            
            # Save as sql_<tablename>.csv
            file_name = f"sql_{table.replace(' ', '_').lower()}.csv"
            output_path = os.path.join(RAW_DIR, file_name)
            
            df.to_csv(output_path, index=False)
            print(f" SQL Server: {table} -> {file_name} ({df.shape[0]} rows)")
        except Exception as e:
            # Your friend ignores SQL errors in the screenshot, but we can print them
            pass 

def extract_from_access():
    conn = get_access_connection()
    if not conn:
        print(" [Access] Connection failed.")
        return

    for table in TABLES:
        try:
            query_table = f"[{table}]"
            # Access sometimes needs specific query structure
            query = f"SELECT * FROM {query_table}"
            
            df = pd.read_sql(query, conn)
            
            # Save as access_<tablename>.csv
            file_name = f"access_{table.replace(' ', '_').lower()}.csv"
            output_path = os.path.join(RAW_DIR, file_name)
            
            df.to_csv(output_path, index=False)
            
            # Print EXACTLY like your friend's screenshot
            print(f"Access:     {table} -> {file_name} ({df.shape[0]} rows)")
        except Exception as e:
            # Print the error EXACTLY like your friend's screenshot
            print(f" Access Error ({table}): {e}")
    
    conn.close()

# This function allows etl_main.py to still work
def run_full_extraction():
    extract_from_sql_server()
    extract_from_access()
    return True

if __name__ == "__main__":
    run_full_extraction()