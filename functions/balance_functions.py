# balance_functions.py
from .db_connection import create_connection, close_connection

def get_balance():
    """Retrieve the current balance from the database."""
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT current_balance FROM balance WHERE id = 1"
    cursor.execute(query)
    
    result = cursor.fetchone()
    close_connection(connection)
    
    if result:
        return result[0]
    else:
        # Handle error appropriately, e.g., raise an exception or return a default value.
        return 0.00

def update_balance(amount):
    """Update the balance in the database by a specified amount. 
    This function can be used for both additions and subtractions based on the passed amount.
    """
    current_balance = get_balance()
    
    # Convert both values to float before addition
    new_balance = float(current_balance) + float(amount)

    connection = create_connection()
    cursor = connection.cursor()

    query = "UPDATE balance SET current_balance = %s WHERE id = 1"
    cursor.execute(query, (new_balance,))
    connection.commit()
    close_connection(connection)

    return new_balance

def set_balance(new_balance):
    """Directly set the balance in the database to the specified value."""
    connection = create_connection()
    cursor = connection.cursor()

    query = "UPDATE balance SET current_balance = %s WHERE id = 1"
    cursor.execute(query, (new_balance,))
    connection.commit()
    close_connection(connection)

    return new_balance


