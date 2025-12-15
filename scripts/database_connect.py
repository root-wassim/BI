import sqlalchemy
import pyodbc
from config import SERVER_NAME, DATABASE_NAME, DRIVER, ACCESS_DB_PATH

def get_sql_engine():
    """Returns SQLAlchemy engine for SQL Server"""
    try:
        connection_str = (
            f"mssql+pyodbc://{SERVER_NAME}/{DATABASE_NAME}?"
            f"driver={DRIVER}&trusted_connection=yes"
        )
        engine = sqlalchemy.create_engine(connection_str)
        return engine
    except Exception as e:
        return None

def get_access_connection():
    """Returns a raw pyodbc connection for MS Access"""
    try:
        conn_str = fr"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={ACCESS_DB_PATH};"
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        return None