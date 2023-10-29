# file: inventory_functions.py

from .db_connection import create_connection, close_connection

def add_item(item_name, quantity, cost_price, selling_price):  # Added selling_price as a parameter
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO Inventory (ItemName, Quantity, CostPrice, SellingPrice) VALUES (%s, %s, %s, %s)"  # Updated query
    values = (item_name, quantity, cost_price, selling_price)  # Added selling_price to the values tuple
    
    cursor.execute(query, values)
    connection.commit()
    close_connection(connection)

def update_item(item_id, item_name, quantity, cost_price, selling_price):  # Added selling_price as a parameter
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE Inventory SET ItemName = %s, Quantity = %s, CostPrice = %s, SellingPrice = %s WHERE ItemID = %s"  # Updated query
    values = (item_name, quantity, cost_price, selling_price, item_id)  # Adjusted the order and added selling_price to the values tuple
    
    print(f"Updating item with ID: {item_id} using query: {query} with values: {values}")  # DEBUG print statement
    
    cursor.execute(query, values)
    connection.commit()
    close_connection(connection)

def delete_item(item_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM Inventory WHERE ItemID = %s"
    values = (item_id,)
    
    cursor.execute(query, values)
    connection.commit()
    close_connection(connection)

def get_all_items():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM Inventory"
    
    cursor.execute(query)
    result = cursor.fetchall()
    close_connection(connection)

    return result
