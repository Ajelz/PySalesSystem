# file: db_connection.py

import mysql.connector
from mysql.connector import Error
import configparser

# Read the configuration from '../database/config.ini'
config = configparser.ConfigParser()
config.read('../database/config.ini')

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL']['host'],
            user=config['MYSQL']['user'],
            password=config['MYSQL']['password'],
            database=config['MYSQL']['database']
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

# Note: I uncommented the 'connection.close()' line, because it's a good practice to close the connection once done.
