# file: expense_functions.py

from .db_connection import create_connection, close_connection

def add_expense(expense_type, expense_amount):
    connection = create_connection()
    cursor = connection.cursor()

    query = "INSERT INTO Expenses (ExpenseType, ExpenseAmount) VALUES (%s, %s)"
    values = (expense_type, expense_amount)
    cursor.execute(query, values)

    connection.commit()
    close_connection(connection)

def update_expense(expense_id, expense_type, expense_amount):
    connection = create_connection()
    cursor = connection.cursor()

    query = "UPDATE Expenses SET ExpenseType = %s, ExpenseAmount = %s WHERE ExpenseID = %s"
    values = (expense_type, expense_amount, expense_id)
    cursor.execute(query, values)

    connection.commit()
    close_connection(connection)

def delete_expense(expense_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "DELETE FROM Expenses WHERE ExpenseID = %s"
    cursor.execute(query, (expense_id,))
    
    connection.commit()
    close_connection(connection)

def get_all_expenses():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM Expenses"
    cursor.execute(query)
    result = cursor.fetchall()

    close_connection(connection)

    return result

def get_expense_by_id(expense_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM Expenses WHERE ExpenseID = %s"
    cursor.execute(query, (expense_id,))
    result = cursor.fetchone()

    close_connection(connection)

    return result
