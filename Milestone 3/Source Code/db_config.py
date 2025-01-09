import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ABOODSLAPTOP\MSSQLSERVER01;'
        'DATABASE=CarDealership;'  # Replace with your database name
        'Trusted_Connection=yes;'  # Use Windows Authentication
    )
    return conn
