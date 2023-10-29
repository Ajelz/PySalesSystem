# file: sales_functions.py
from .db_connection import create_connection, close_connection

def add_sale(item_id, quantity_sold, selling_price):
    connection = create_connection()
    cursor = connection.cursor()

    # First, let's adjust the Inventory quantity for this item.
    query = "UPDATE Inventory SET Quantity = Quantity - %s WHERE ItemID = %s"
    values = (quantity_sold, item_id)
    cursor.execute(query, values)

    # Now, let's record the sale.
    query = "INSERT INTO Sales (ItemID, QuantitySold, SellingPrice) VALUES (%s, %s, %s)"
    values = (item_id, quantity_sold, selling_price)
    cursor.execute(query, values)

    connection.commit()
    close_connection(connection)


def update_sale(sale_id, item_id, quantity_sold, selling_price):
    connection = create_connection()
    cursor = connection.cursor()

    # Adjust Inventory based on updated sales. This is more complicated than in add_sale.
    # Here, we first retrieve the original sale record.
    query = "SELECT ItemID, QuantitySold FROM Sales WHERE SaleID = %s"
    cursor.execute(query, (sale_id,))
    original_sale = cursor.fetchone()

    # Return quantities from original sale to Inventory
    query = "UPDATE Inventory SET Quantity = Quantity + %s WHERE ItemID = %s"
    values = (original_sale[1], original_sale[0])
    cursor.execute(query, values)

    quantity_sold = int(quantity_sold)

    # Check if the updated quantity will exceed available inventory
    query = "SELECT Quantity FROM Inventory WHERE ItemID = %s"
    cursor.execute(query, (item_id,))
    available_quantity = cursor.fetchone()[0]

    if quantity_sold > available_quantity:
        close_connection(connection)
        return False, "Unable to update sale as the desired quantity exceeds the available stock."

    # Subtract new quantities from Inventory
    query = "UPDATE Inventory SET Quantity = Quantity - %s WHERE ItemID = %s"
    values = (quantity_sold, item_id)
    cursor.execute(query, values)

    # Finally, update the sale record
    query = "UPDATE Sales SET ItemID = %s, QuantitySold = %s, SellingPrice = %s WHERE SaleID = %s"
    values = (item_id, quantity_sold, selling_price, sale_id)
    cursor.execute(query, values)

    connection.commit()
    close_connection(connection)

    return True, "Success"

def delete_sale(sale_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Fetch the quantities and ItemID for the sale to be deleted.
        query = "SELECT ItemID, QuantitySold FROM Sales WHERE SaleID = %s"
        cursor.execute(query, (sale_id,))
        original_sale = cursor.fetchone()

        if not original_sale:
            # If the sale is not found, return None.
            close_connection(connection)
            return None

        query = "UPDATE Inventory SET Quantity = Quantity + %s WHERE ItemID = %s"
        values = (original_sale[1], original_sale[0])  # original_sale[1] is QuantitySold, original_sale[0] is ItemID
        cursor.execute(query, values)

        # Delete the sale
        query = "DELETE FROM Sales WHERE SaleID = %s"
        cursor.execute(query, (sale_id,))

        connection.commit()
        close_connection(connection)
        
        # Return the quantity that was sold (which has been added back to the inventory).
        return original_sale[1]
    except Exception as e:
        print(f"Error deleting sale: {e}")  # Optionally log the error for debugging
        close_connection(connection)
        return None  # An error occurred



def get_all_sales():
    connection = create_connection()
    cursor = connection.cursor()
    
    # Adjusted query to join sales with inventory on ItemID and select necessary columns, including SellingPrice and CostPrice
    query = """
        SELECT s.SaleID, s.ItemID, i.ItemName, s.QuantitySold, s.SellingPrice, 
               (s.SellingPrice - (s.QuantitySold * i.CostPrice)) AS Profit
        FROM Sales s
        JOIN Inventory i ON s.ItemID = i.ItemID;
    """
    
    cursor.execute(query)
    result = cursor.fetchall()

    close_connection(connection)

    return result


def get_sale_by_id(sale_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM Sales WHERE SaleID = %s"
    cursor.execute(query, (sale_id,))
    result = cursor.fetchone()

    close_connection(connection)

    return result

def get_all_inventory_items():
    connection = create_connection()
    cursor = connection.cursor()
    
    # Fetching ItemID, ItemName, Quantity, and SellingPrice
    query = "SELECT ItemID, ItemName, Quantity, SellingPrice FROM Inventory"
    cursor.execute(query)
    raw_results = cursor.fetchall()

    # Adjusting the format for each result
    formatted_results = [(item[0], "{} ({})".format(item[1], item[2]), item[3]) for item in raw_results]

    close_connection(connection)
    return formatted_results


def get_selling_price_by_id(item_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT SellingPrice FROM Inventory WHERE ItemID = %s"
    cursor.execute(query, (item_id,))
    result = cursor.fetchone()
    close_connection(connection)
    return result[0] if result else None

