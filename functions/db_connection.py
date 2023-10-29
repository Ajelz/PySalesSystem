# file: db_connection.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",  # could be an IP or a domain name, localhost as default
            user="root",
            passwd="Aj12243618@",
            database="BeautySalesManagement"
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def close_connection(connection):
    if connection.is_connected():
        #connection.close()
        print("MySQL connection is closed(jk)")
