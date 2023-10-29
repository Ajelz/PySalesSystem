from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
import sys
from functions.sales_functions import get_all_inventory_items, get_selling_price_by_id, add_sale, get_all_sales, delete_sale, update_sale
from dialogs.add_sale_dialog import AddSaleDialog
from dialogs.delete_sale_dialog import DeleteSaleDialog
from dialogs.edit_sale_dialog import EditSaleDialog

class SalesManagement(QWidget):
    sale_updated_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Sales Management")
        self.setGeometry(100, 100, 800, 600)

        # Define layout
        self.layout = QVBoxLayout()

        # Create the table
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Adjusted for the new column
        self.table.setHorizontalHeaderLabels(["Sale ID", "Item ID", "Item Name", "Quantity Sold", "Total Selling Price", "Profit"])

        # Create the buttons
        self.addButton = QPushButton("Add Sale")
        self.editButton = QPushButton("Edit Sale")
        self.deleteButton = QPushButton("Delete Sale")

        # Connect buttons to their functions
        self.addButton.clicked.connect(self.add_sale)
        self.editButton.clicked.connect(self.edit_sale)
        self.deleteButton.clicked.connect(self.delete_sale)

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

    def add_sale(self):
        dialog = AddSaleDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            sale_data = dialog.get_input_values()
            try:
                item_id = int(sale_data["item_id"])
                quantity = int(sale_data["quantity"])
                selling_price = get_selling_price_by_id(item_id)  # Fetch the selling price from inventory

                if selling_price is not None:
                    add_sale(item_id, quantity, selling_price * quantity)
                    self.load_data()
                    self.sale_updated_signal.emit()  # Refresh the inventory table or view
                else:
                    QMessageBox.critical(self, "Error", "Failed to get the selling price!")
            except ValueError:
                QMessageBox.critical(self, "Error", "Please enter valid data!")


    def edit_sale(self):
        # Get the selected sale
        selected_row = self.table.currentRow()

        if selected_row != -1:  # A sale is selected
            # Get the sale details
            sale_id = self.table.item(selected_row, 0).text()
            item_id = self.table.item(selected_row, 1).text()

            quantity_sold = self.table.item(selected_row, 3).text()
            # Open the EditSaleDialog with the sale details
            dialog = EditSaleDialog(item_id, quantity_sold)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                # Retrieve edited values from the dialog
                edited_values = dialog.get_input_values()
                selling_price = get_selling_price_by_id(edited_values['item_id'])
                edited_values['selling_price'] = selling_price

                # Call your backend function to edit the sale
                success, message = update_sale(sale_id, edited_values['item_id'], edited_values['quantity'], edited_values['selling_price'])

                if success:
                    QMessageBox.information(self, "Success", "Sale was successfully updated!")
                    self.load_data()  # Refresh the table
                    self.sale_updated_signal.emit()  # Refresh the inventory table or view
                else:
                    QMessageBox.critical(self, "Error", message)



    def delete_sale(self):
        # Get the selected sale
        selected_row = self.table.currentRow()

        if selected_row != -1:  # A sale is selected
            # Get the sale details
            sale_id = self.table.item(selected_row, 0).text()
            item_id = self.table.item(selected_row, 1).text()

            # Open the DeleteSaleDialog with the sale details
            dialog = DeleteSaleDialog(sale_id)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                # Call your backend function delete_sale here
                returned_quantity = delete_sale(sale_id)

                if returned_quantity is not None:  # If the function did not return None, it was successful
                    QMessageBox.information(self, "Success", f"Sale with ID {sale_id} was successfully deleted and {returned_quantity} items were returned to the inventory!")
                    self.load_data()  # Refresh the table
                    self.sale_updated_signal.emit()  # Refresh the inventory table or view
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete the sale!")



    def load_data(self):
        # Step 1: Fetch the data
        sales_data = get_all_sales()

        # Step 2: Clear the table
        self.table.setRowCount(0)  # Reset the number of rows in the table

        # Step 3: Populate the table
        for sale in sales_data:
            # Append a new row to the table
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            # Fill the row with sales data
            for col, data in enumerate(sale):
                # Ensure the profit value (and any other floats) is displayed with two decimal places
                value = "{:.2f}".format(data) if isinstance(data, float) else str(data)
                self.table.setItem(row_position, col, QTableWidgetItem(value))



if __name__ == "__main__":
    app = QApplication(sys.argv)

    sales_management = SalesManagement()
    sales_management.show()

    sys.exit(app.exec_())
