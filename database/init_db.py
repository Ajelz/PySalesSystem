import mysql.connector
from mysql.connector import Error
import os
import pytoml as toml

# Construct the base directory and paths based on the script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_PATH = os.path.join(BASE_DIR, 'init_db.sql')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.toml')

# Read the configuration from the adjusted path
with open(CONFIG_PATH, 'r') as config_file:
    config = toml.load(config_file)

def init_database():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL']['host'],
            user=config['MYSQL']['user'],
            password=config['MYSQL']['password']
        )
        cursor = connection.cursor()

        # Reading and executing the SQL file
        with open(SQL_PATH, "r") as file:
            sql_script = file.read()
            commands = sql_script.split(";")
            for command in commands:
                command = command.strip()
                if command:
                    print("Executing SQL command:", command)  # Debugging print
                    cursor.execute(command)

        print("Database initialized successfully.")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    init_database()
