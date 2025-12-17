import os

# --- Database Settings ---
SERVER_NAME = r'.\SQLEXPRESS'  # Verify this is your SQL Server name
DATABASE_NAME = 'Northwind'
DRIVER = 'ODBC Driver 17 for SQL Server'
TRUSTED_CONNECTION = 'yes'

# Access Database Name
ACCESS_FILE_NAME = 'Northwind 2012.accdb'

# --- Project Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# File Paths
ACCESS_DB_PATH = os.path.join(DATA_DIR, ACCESS_FILE_NAME)
SQL_FILE_PATH = os.path.join(DATA_DIR, 'sqlserver.sql')  # <--- This was missing

# Data Subfolders
RAW_DIR = os.path.join(DATA_DIR, 'raw')
STAGING_DIR = os.path.join(DATA_DIR, 'staging')
WAREHOUSE_DIR = os.path.join(DATA_DIR, 'warehouse')