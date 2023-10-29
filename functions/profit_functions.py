# file: profit_functions.py

from .db_connection import create_connection, close_connection
from .sales_functions import get_all_sales
from .expense_functions import get_all_expenses

def calculate_profit():
    connection = create_connection()
    cursor = connection.cursor()

    # Get all sales and calculate total income
    sales = get_all_sales()
    total_income = sum(sale[5] for sale in sales)

    # Get all expenses and calculate total expenses
    expenses = get_all_expenses()
    total_expenses = sum(expense[2] for expense in expenses)  # expense[2] is ExpenseAmount

    # Calculate profit
    profit = total_income - total_expenses
    print(profit)

    close_connection(connection)

    return profit
