from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QMessageBox, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
import sys
from functions.sales_functions import get_all_inventory_items, get_selling_price_by_id, add_sale, get_all_sales, delete_sale, update_sale
from dialogs.add_sale_dialog import AddSaleDialog
from dialogs.delete_sale_dialog import DeleteSaleDialog
from dialogs.edit_sale_dialog import EditSaleDialog
from functions.balance_functions import get_balance, update_balance
from windows.SalesManagementUI import SalesManagementUI


class SalesManagement(SalesManagementUI):
    sale_updated_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

        # Connect buttons to their functions
        self.addButton.clicked.connect(self.add_sale)
        self.editButton.clicked.connect(self.edit_sale)
        self.deleteButton.clicked.connect(self.delete_sale)

        # Load data from the database
        self.load_data()


    def add_sale(self):
        dialog = AddSaleDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            sale_data = dialog.get_input_values()
            try:
                item_id = int(sale_data["item_id"])
                quantity = int(sale_data["quantity"])
                selling_price_per_item = get_selling_price_by_id(item_id)
                total_selling_price = selling_price_per_item * quantity
                
                if selling_price_per_item is not None:
                    add_sale(item_id, quantity, total_selling_price)
                    update_balance(total_selling_price)
                    self.load_data()
                    self.sale_updated_signal.emit() 
                    self.main_window.balance_updated.emit()
                else:
                    QMessageBox.critical(self, "Error", "Failed to get the selling price!")
            except ValueError:
                QMessageBox.critical(self, "Error", "Please enter valid data!")


    def edit_sale(self):
        selected_row = self.table.currentRow()

        if selected_row != -1:  # A sale is selected
            sale_id = self.table.item(selected_row, 0).text()
            prev_quantity_sold = int(self.table.item(selected_row, 3).text())
            prev_total_selling_price = float(self.table.item(selected_row, 4).text())

            dialog = EditSaleDialog(sale_id, prev_quantity_sold)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                edited_values = dialog.get_input_values()
                new_quantity = int(edited_values['quantity'])
                selling_price_per_item = get_selling_price_by_id(edited_values['item_id'])
                new_total_selling_price = selling_price_per_item * new_quantity
                
                difference_in_price = float(new_total_selling_price) - prev_total_selling_price

                success, message = update_sale(sale_id, edited_values['item_id'], new_quantity, new_total_selling_price)

                if success:
                    update_balance(difference_in_price)  # Adjust the balance with the price difference
                    QMessageBox.information(self, "Success", "Sale was successfully updated!")
                    self.load_data()  
                    self.sale_updated_signal.emit()
                    self.main_window.balance_updated.emit()
                else:
                    QMessageBox.critical(self, "Error", message)



    def delete_sale(self):
        selected_row = self.table.currentRow()

        if selected_row != -1:
            sale_id = self.table.item(selected_row, 0).text()
            total_selling_price = float(self.table.item(selected_row, 4).text())

            dialog = DeleteSaleDialog(sale_id)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                returned_quantity = delete_sale(sale_id)

                if returned_quantity is not None:
                    update_balance(-total_selling_price)  # Deduct the selling price
                    QMessageBox.information(self, "Success", f"Sale with ID {sale_id} was successfully deleted and {returned_quantity} items were returned to the inventory!")
                    self.load_data()  
                    self.sale_updated_signal.emit()
                    self.main_window.balance_updated.emit()
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete the sale!")



    def load_data(self):
        sales_data = get_all_sales()
        self.table.setRowCount(0)
        self.balanceLabel.setText(f"Balance: {get_balance():.2f} LYD")
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
