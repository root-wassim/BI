import pandas as pd
import os
from config import STAGING_DIR, WAREHOUSE_DIR

# Ensure warehouse directory exists
os.makedirs(WAREHOUSE_DIR, exist_ok=True)

def generate_schema_sql(tables):
    sql_statements = []
    # Primary Keys definition
    pks = {
        'DimDate': 'sk_date', 
        'DimClient': 'sk_client', 
        'DimEmployee': 'sk_employee', 
        'FactSales': 'fact_id'
    }

    print("... Generating schema.sql")
    for table_name, df in tables.items():
        columns = []
        for col, dtype in df.dtypes.items():
            sql_type = "INT" if "int" in str(dtype) else "DECIMAL(10,2)" if "float" in str(dtype) else "DATE" if "datetime" in str(dtype) else "VARCHAR(255)"
            if col == pks.get(table_name): sql_type += " PRIMARY KEY"
            columns.append(f"    {col} {sql_type}")
        sql_statements.append(f"CREATE TABLE {table_name} (\n" + ",\n".join(columns) + "\n);\n")
    
    with open(os.path.join(WAREHOUSE_DIR, "schema.sql"), "w") as f:
        f.write("\n".join(sql_statements))

def load_to_warehouse():
    print("\n--- Starting Load (Staging -> Warehouse) ---")
    
    # MAPPING: Staging File -> Final Table Name
    # DimProduct is REMOVED as requested
    file_mapping = {
        'cleaned_date': 'DimDate',
        'cleaned_clients': 'DimClient',
        'cleaned_employees': 'DimEmployee',
        'cleaned_sales': 'FactSales'
    }

    loaded_tables = {}

    for csv_name, table_name in file_mapping.items():
        csv_path = os.path.join(STAGING_DIR, f"{csv_name}.csv")
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            loaded_tables[table_name] = df
            
            # Save as Final Table in Warehouse
            df.to_csv(os.path.join(WAREHOUSE_DIR, f"{table_name}.csv"), index=False)
            df.to_parquet(os.path.join(WAREHOUSE_DIR, f"{table_name}.parquet"), index=False)
            
            print(f"Transformed {csv_name} \t-> Loaded into {table_name} ({len(df)} rows)")
        else:
            print(f"Missing staging file: {csv_name}")

    if loaded_tables:
        generate_schema_sql(loaded_tables)

    print("\n Load Complete! Data Warehouse is ready.")

if __name__ == "__main__":
    load_to_warehouse()