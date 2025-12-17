import pandas as pd
import os
import glob
from config import RAW_DIR, STAGING_DIR

os.makedirs(STAGING_DIR, exist_ok=True)

def clean_col_names(df):
    if df is not None:
        df.columns = [c.lower().strip().replace(' ', '').replace('_', '') for c in df.columns]
    return df

def load_raw_data(table_name, pk_cols):
    dfs = []
    pattern = os.path.join(RAW_DIR, f"*_{table_name}.csv")
    files = glob.glob(pattern)
    print(f"   - Found {len(files)} source files for '{table_name}'")

    for f in files:
        try:
            df = pd.read_csv(f)
            df = clean_col_names(df) 
            dfs.append(df)
        except Exception as e:
            print(f" Error loading {f}: {e}")
    
    if not dfs: return pd.DataFrame()
    
    merged_df = pd.concat(dfs, ignore_index=True)
    clean_pks = [c.lower() for c in pk_cols]
    
    if set(clean_pks).issubset(merged_df.columns):
        merged_df = merged_df.drop_duplicates(subset=clean_pks, keep='first')
        
    return merged_df

def create_intermediate_master(orders, details, customers, employees, products):
    # Just for debugging/staging visualization
    master = pd.merge(details, orders, on='orderid', how='inner')
    if not customers.empty: master = pd.merge(master, customers, on='customerid', how='left', suffixes=('', '_cust'))
    if not employees.empty: master = pd.merge(master, employees, on='employeeid', how='left', suffixes=('', '_emp'))
    if not products.empty: master = pd.merge(master, products, on='productid', how='left', suffixes=('', '_prod'))
    return master

def transform_dim_date(orders_df):
    print("... Creating DimDate")
    if orders_df.empty: return pd.DataFrame()
    
    orders_df['orderdate'] = orders_df['orderdate'].astype(str)
    try: dates = pd.to_datetime(orders_df['orderdate'], format='mixed', errors='coerce').dropna().unique()
    except: dates = pd.to_datetime(orders_df['orderdate'], infer_datetime_format=True, errors='coerce').dropna().unique()
    
    date_df = pd.DataFrame({'full_date': dates})
    date_df = date_df.sort_values('full_date')
    
    date_df['sk_date'] = date_df['full_date'].dt.strftime('%Y%m%d').astype(int)
    date_df['year'] = date_df['full_date'].dt.year
    date_df['month'] = date_df['full_date'].dt.month
    date_df['month_name'] = date_df['full_date'].dt.month_name()
    date_df['quarter'] = date_df['full_date'].dt.quarter
    
    return date_df

def transform_dim_client(customers_df):
    print("... Creating DimClient")
    if customers_df.empty: return pd.DataFrame()
    dim = customers_df.copy()
    dim = dim.rename(columns={'customerid': 'bk_customer_id', 'companyname': 'company_name'})
    dim['bk_customer_id'] = dim['bk_customer_id'].astype(str).str.upper().str.strip()
    for col in ['city', 'country', 'region']:
        if col not in dim.columns: dim[col] = 'Unknown'
    dim['sk_client'] = range(1, len(dim) + 1)
    cols = ['sk_client', 'bk_customer_id', 'company_name', 'city', 'country', 'region']
    return dim[[c for c in cols if c in dim.columns]]

def enrich_employee_with_territories(dim_emp, emp_terr_df, terr_df, region_df):
    if emp_terr_df.empty or terr_df.empty:
        dim_emp['territories'] = 'Unknown'
        dim_emp['sales_region'] = 'Unknown'
        return dim_emp
    merged = pd.merge(emp_terr_df, terr_df, on='territoryid', how='left')
    if not region_df.empty and 'regionid' in merged.columns:
        merged = pd.merge(merged, region_df, on='regionid', how='left')
        region_col = 'regiondescription'
    else:
        merged['regiondescription'] = 'Unknown'
        region_col = 'regiondescription'
    
    if 'territorydescription' in merged.columns: merged['territorydescription'] = merged['territorydescription'].astype(str).str.strip()
    if region_col in merged.columns: merged[region_col] = merged[region_col].astype(str).str.strip()
    
    terr_grouped = merged.groupby('employeeid')['territorydescription'].apply(lambda x: ', '.join(x)).reset_index(name='territories')
    region_grouped = merged.groupby('employeeid')[region_col].apply(lambda x: ', '.join(set(x))).reset_index(name='sales_region')
    
    dim_emp = pd.merge(dim_emp, terr_grouped, left_on='bk_employee_id', right_on='employeeid', how='left')
    dim_emp = pd.merge(dim_emp, region_grouped, left_on='bk_employee_id', right_on='employeeid', how='left')
    
    dim_emp['territories'] = dim_emp['territories'].fillna('No Territory')
    dim_emp['sales_region'] = dim_emp['sales_region'].fillna('No Region')
    return dim_emp.drop(columns=['employeeid_x', 'employeeid_y'], errors='ignore')

def transform_dim_employee(employees_df, emp_terr_df, terr_df, region_df):
    print("... Creating DimEmployee")
    if employees_df.empty: return pd.DataFrame()
    dim = employees_df.copy()
    dim = dim.rename(columns={'employeeid': 'bk_employee_id', 'firstname': 'first_name', 'lastname': 'last_name'})
    dim['Employee_name'] = dim['first_name'].astype(str) + ' ' + dim['last_name'].astype(str)
    dim['sk_employee'] = range(1, len(dim) + 1)
    dim = enrich_employee_with_territories(dim, emp_terr_df, terr_df, region_df)
    cols = ['sk_employee', 'bk_employee_id', 'Employee_name', 'title', 'city', 'country', 'sales_region', 'territories']
    return dim[[c for c in cols if c in dim.columns]]



#  UPDATED FACT FUNCTION
def transform_fact_sales(orders_df, details_df, dim_client, dim_emp): # removed dim_prod arg
    print("... Creating FactSales")
    if orders_df.empty or details_df.empty: return pd.DataFrame()
    
    fact = pd.merge(details_df, orders_df, on='orderid', how='inner')
    
    # Calculate Amount
    if 'unitprice_x' in fact.columns: price_col = 'unitprice_x'
    elif 'unitprice' in fact.columns: price_col = 'unitprice'
    else: return pd.DataFrame()
    fact['total_amount'] = (fact[price_col] * fact['quantity']) * (1 - fact['discount'])
    
    # Delivery Status
    fact['delivery_status'] = fact['shippeddate'].apply(lambda x: 'Livrée' if pd.notnull(x) and str(x).strip() != '' else 'Non Livrée')
    
    # Clean FK
    if 'customerid' in fact.columns:
        fact['customerid'] = fact['customerid'].astype(str).str.upper().str.strip()

    # Link Dimensions
    if not dim_client.empty:
        fact = pd.merge(fact, dim_client[['bk_customer_id', 'sk_client']], left_on='customerid', right_on='bk_customer_id', how='left')
    if not dim_emp.empty:
        fact = pd.merge(fact, dim_emp[['bk_employee_id', 'sk_employee']], left_on='employeeid', right_on='bk_employee_id', how='left')
    
    # Date Key
    fact['orderdate'] = fact['orderdate'].astype(str)
    try: fact['dt'] = pd.to_datetime(fact['orderdate'], format='mixed', errors='coerce')
    except: fact['dt'] = pd.to_datetime(fact['orderdate'], infer_datetime_format=True, errors='coerce')
    fact['sk_date'] = fact['dt'].dt.strftime('%Y%m%d').fillna(19000101).astype(int)

    fact = fact.rename(columns={'orderid': 'bk_order_id', price_col: 'unit_price'})
    fact['fact_id'] = range(1, len(fact) + 1)
    
    #  FINAL COLUMNS 
    final_cols = ['fact_id', 'bk_order_id', 'sk_client', 'sk_employee', 'sk_date', 
                  'quantity', 'unit_price', 'discount', 'total_amount', 'delivery_status', ]
    
    return fact[[c for c in final_cols if c in fact.columns]]

# UPDATED RUN FUNCTION 
def run_transformation():
    print("\n--- Starting Transformation (3 Dimensions Only) ---")
    
    orders = load_raw_data('orders', ['orderid'])
    details = load_raw_data('order_details', ['orderid', 'productid']) 
    customers = load_raw_data('customers', ['customerid'])
    employees = load_raw_data('employees', ['employeeid'])
    
    # Optional: Load extra employee tables for the HR view
    emp_terr = load_raw_data('employeeterritories', ['employeeid', 'territoryid'])
    territories = load_raw_data('territories', ['territoryid'])
    region = load_raw_data('region', ['regionid'])

    # Create Dimensions
    dim_date = transform_dim_date(orders)
    dim_client = transform_dim_client(customers)
    dim_emp = transform_dim_employee(employees, emp_terr, territories, region)
    
    # Create Fact
    fact_sales = transform_fact_sales(orders, details, dim_client, dim_emp)
    
    print("\n--- Saving Staging Files ---")
    dim_date.to_csv(os.path.join(STAGING_DIR, 'cleaned_date.csv'), index=False)
    dim_client.to_csv(os.path.join(STAGING_DIR, 'cleaned_clients.csv'), index=False)
    dim_emp.to_csv(os.path.join(STAGING_DIR, 'cleaned_employees.csv'), index=False)
    fact_sales.to_csv(os.path.join(STAGING_DIR, 'cleaned_sales.csv'), index=False)
    
    print("\n Transformation Complete!")