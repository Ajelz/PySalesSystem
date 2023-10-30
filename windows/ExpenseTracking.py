from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt
import sys
from dialogs.add_expense_dialog import AddExpenseDialog
from dialogs.edit_expense_dialog import EditExpenseDialog
from dialogs.delete_expense_dialog import DeleteExpenseDialog
from functions.expense_functions import get_all_expenses, add_expense, update_expense, delete_expense

class ExpenseTracking(QWidget):
    def __init__(self):
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Expense Tracking")
        self.setGeometry(100, 100, 800, 600)

        # Define layout
        self.layout = QVBoxLayout()

        # Create the table
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Set three columns for Expense ID, Expense Type, and Expense Amount
        self.table.setHorizontalHeaderLabels(["Expense ID", "Expense Type", "Expense Amount"])  # Set the headers

        # Create the buttons
        self.addButton = QPushButton("Add Expense")
        self.editButton = QPushButton("Edit Expense")
        self.deleteButton = QPushButton("Delete Expense")

        # Connect buttons to their functions
        self.addButton.clicked.connect(self.add_expense)
        self.editButton.clicked.connect(self.edit_expense)
        self.deleteButton.clicked.connect(self.delete_expense)

        # Add widgets to layout
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.editButton)
        self.layout.addWidget(self.deleteButton)

        # Set the layout
        self.setLayout(self.layout)

        # Load data from the database
        self.load_data()

    # Functions to be connected to the buttons

    def add_expense(self):
        # Open the AddExpenseDialog
        dialog = AddExpenseDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            expense_type, expense_amount = dialog.get_values()  # Retrieve values entered
            add_expense(expense_type, expense_amount)  # Pass values to backend function
            self.load_data()  # Refresh the table to show newly added expense

    def edit_expense(self):
        # Get the selected expense
        selected_row = self.table.currentRow()

        if selected_row != -1:
            expense_id = self.table.item(selected_row, 0).text() if self.table.item(selected_row, 0) else None
            expense_type = self.table.item(selected_row, 1).text() if self.table.item(selected_row, 1) else None
            expense_amount = self.table.item(selected_row, 2).text() if self.table.item(selected_row, 2) else None

            if not all([expense_id, expense_type, expense_amount]):
                # If any of the above values are None, it means the row is incomplete.
                # Handle this case accordingly.
                print("Incomplete data in the selected row.")
                return

            dialog = EditExpenseDialog(expense_id, expense_type, expense_amount)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                data = dialog.get_data()
                updated_id = data['expense_id']
                updated_type = data['type']
                updated_amount = data['amount']

                update_expense(updated_id, updated_type, updated_amount)

            self.load_data()


    def delete_expense(self):
        # Get the selected expense
        selected_row = self.table.currentRow()

        if selected_row != -1:  # An expense is selected
            # Get the expense details
            expense_id = self.table.item(selected_row, 0).text()
            expense_type = self.table.item(selected_row, 1).text()

            # Open the DeleteExpenseDialog with the expense details
            dialog = DeleteExpenseDialog(expense_id, expense_type)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                # Call your backend function to delete the expense
                delete_expense(expense_id)  # Assuming you have this function

                # Refresh the table
                self.load_data()


    def load_data(self):
        expenses = get_all_expenses()  # Retrieve all expenses from the database

        self.table.setRowCount(0)  # Clear current table rows
        for expense in expenses:
            row_position = self.table.rowCount()  # Get the current number of rows
            self.table.insertRow(row_position)  # Insert a new row at the bottom

            # Populate the table with the expense data
            self.table.setItem(row_position, 0, QTableWidgetItem(str(expense[0])))  # ExpenseID
            self.table.setItem(row_position, 1, QTableWidgetItem(expense[1]))      # ExpenseType
            self.table.setItem(row_position, 2, QTableWidgetItem(str(expense[2])))  # ExpenseAmount


if __name__ == "__main__":
    app = QApplication(sys.argv)

    expense_tracking = ExpenseTracking()
    expense_tracking.show()

    sys.exit(app.exec_())
