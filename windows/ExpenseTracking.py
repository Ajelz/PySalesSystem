from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import sys
# Import your backend functions
# from expense_functions import get_expenses, add_expense, edit_expense, delete_expense

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
        # self.load_data()

    # Functions to be connected to the buttons

    def add_expense(self):
        # Open the AddExpenseDialog
        dialog = AddExpenseDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            # TODO: Call your backend function add_expense here
            pass

    def edit_expense(self):
        # Get the selected expense
        selected_row = self.table.currentRow()

        if selected_row != -1:  # An expense is selected
            # Get the expense details
            expense_id = self.table.item(selected_row, 0).text()
            expense_type = self.table.item(selected_row, 1).text()
            expense_amount = self.table.item(selected_row, 2).text()

            # Open the EditExpenseDialog with the expense details
            dialog = EditExpenseDialog(expense_id, expense_type, expense_amount)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                # TODO: Call your backend function edit_expense here
                pass

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
                # TODO: Call your backend function delete_expense here
                pass

    # def load_data(self):
        # TODO: Implement load_data function
        # This function should load the data from the expense database and populate the table
        # The get_expenses function from expense_functions can be used to retrieve the data
        # pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    expense_tracking = ExpenseTracking()
    expense_tracking.show()

    sys.exit(app.exec_())
