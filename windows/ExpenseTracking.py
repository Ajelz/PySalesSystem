# ExpenseTracking.py
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
import sys

from dialogs.add_expense_dialog import AddExpenseDialog
from dialogs.edit_expense_dialog import EditExpenseDialog
from dialogs.delete_expense_dialog import DeleteExpenseDialog
from functions.expense_functions import get_all_expenses, add_expense, update_expense, delete_expense
from functions.balance_functions import get_balance, update_balance
from windows.ExpenseTrackingUI import ExpenseTrackingUI 

class ExpenseTracking(ExpenseTrackingUI):
    expense_updated_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Connect buttons to their functions
        self.addButton.clicked.connect(self.add_expense)
        self.editButton.clicked.connect(self.edit_expense)
        self.deleteButton.clicked.connect(self.delete_expense)

        # Load data from the database
        self.load_data()

    def add_expense(self):
        dialog = AddExpenseDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            expense_type, expense_amount = dialog.get_values()  # Retrieve values entered
            add_expense(expense_type, expense_amount)  # Pass values to backend function
            update_balance(-float(expense_amount))  # Deducting the expense from the balance
            self.load_data()  # Refresh the table to show newly added expense
            self.expense_updated_signal.emit()
            self.main_window.balance_updated.emit()

    def edit_expense(self):
        selected_row = self.table.currentRow()

        if selected_row != -1:
            expense_id = self.table.item(selected_row, 0).text()
            prev_expense_amount = float(self.table.item(selected_row, 2).text())

            dialog = EditExpenseDialog(expense_id, self.table.item(selected_row, 1).text(), prev_expense_amount)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                data = dialog.get_data()
                new_expense_amount = float(data['amount'])
                
                difference_in_amount = new_expense_amount - prev_expense_amount

                update_expense(data['expense_id'], data['type'], new_expense_amount)
                update_balance(-difference_in_amount)  # Adjust the balance with the amount difference
                self.load_data()
                self.expense_updated_signal.emit()
                self.main_window.balance_updated.emit()

    def delete_expense(self):
        selected_row = self.table.currentRow()

        if selected_row != -1:  # An expense is selected
            expense_id = self.table.item(selected_row, 0).text()
            expense_amount = float(self.table.item(selected_row, 2).text())

            dialog = DeleteExpenseDialog(expense_id, self.table.item(selected_row, 1).text())
            result = dialog.exec_()

            if result == QDialog.Accepted:
                delete_expense(expense_id)
                update_balance(expense_amount)  # Adding back the deleted expense amount to the balance
                self.load_data()
                self.expense_updated_signal.emit()
                self.main_window.balance_updated.emit()

    def load_data(self):
        expenses = get_all_expenses()  # Retrieve all expenses from the database

        self.table.setRowCount(0)  # Clear current table rows
        self.balanceLabel.setText(f"Balance: {get_balance():.2f} LYD")
        for expense in expenses:
            row_position = self.table.rowCount()  # Get the current number of rows
            self.table.insertRow(row_position)  # Insert a new row at the bottom

            # Populate the table with the expense data
            self.table.setItem(row_position, 0, QTableWidgetItem(str(expense[0])))  # ExpenseID
            self.table.setItem(row_position, 1, QTableWidgetItem(expense[1]))      # ExpenseType
            self.table.setItem(row_position, 2, QTableWidgetItem("{:.2f}".format(expense[2])))  # ExpenseAmount

if __name__ == "__main__":
    app = QApplication(sys.argv)

    expense_tracking = ExpenseTracking()
    expense_tracking.show()

    sys.exit(app.exec_())
