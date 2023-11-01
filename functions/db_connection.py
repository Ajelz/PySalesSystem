import mysql.connector
from mysql.connector import Error
import os
import sys
import pytoml

# Check if we're running as a bundled application or as a script
if getattr(sys, 'frozen', False):
    # If bundled with PyInstaller
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one directory

config_path = os.path.join(base_dir, 'database', 'config.toml')

# Read the configuration from the adjusted path
with open(config_path, 'r') as config_file:
    config = pytoml.load(config_file)

def create_connection():
    connection = None
    try:
        # Connect to the specified database
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
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")
