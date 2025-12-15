import os

# --- Database Settings ---
# Update this if you have SQL Server, otherwise keep it as placeholder
SERVER_NAME = 'LOCALHOST'  
DATABASE_NAME = 'Northwind'
DRIVER = 'ODBC Driver 17 for SQL Server'
TRUSTED_CONNECTION = 'yes'

# Access Database Name
ACCESS_FILE_NAME = 'Northwind 2012.accdb'

# --- Project Paths ---
# This calculates the path to your project folder automatically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# File Paths
ACCESS_DB_PATH = os.path.join(DATA_DIR, ACCESS_FILE_NAME)
SQL_FILE_PATH = os.path.join(DATA_DIR, 'sqlserver.sql')

# Data Subfolders
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
WAREHOUSE_DIR = os.path.join(DATA_DIR, 'warehouse')