from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt
import sys
from dialogs import AddItemDialog, EditItemDialog, DeleteItemDialog
from functions.inventory_functions import get_all_items, add_item, update_item, delete_item

class InventoryManagement(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 1000, 600)

        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Item ID", "Item Name", "Quantity", "Cost Price", "Selling Price", "Profit"])

        self.addButton = QPushButton("Add Item")
        self.editButton = QPushButton("Edit Item")
        self.deleteButton = QPushButton("Delete Item")

        self.addButton.clicked.connect(self.add_item)
        self.editButton.clicked.connect(self.edit_item)
        self.deleteButton.clicked.connect(self.delete_item)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.editButton)
        self.layout.addWidget(self.deleteButton)

        self.setLayout(self.layout)

        self.load_data()

    def add_item(self):
        dialog = AddItemDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            data = dialog.get_data()
            item_name = data['name']
            quantity = data['quantity']
            cost_price = data['cost_price']
            selling_price = data['selling_price']

            add_item(item_name, quantity, cost_price, selling_price)

        self.load_data()

    def edit_item(self):
        selected_row = self.table.currentRow()

        if selected_row != -1:
            item_id = self.table.item(selected_row, 0).text() if self.table.item(selected_row, 0) else None
            item_name = self.table.item(selected_row, 1).text() if self.table.item(selected_row, 1) else None
            item_quantity = self.table.item(selected_row, 2).text() if self.table.item(selected_row, 2) else None
            item_cost_price = self.table.item(selected_row, 3).text() if self.table.item(selected_row, 3) else None
            item_selling_price = self.table.item(selected_row, 4).text() if self.table.item(selected_row, 4) else None

            if not all([item_id, item_name, item_quantity, item_cost_price, item_selling_price]):  
                # If any of the above values are None, it means the row is incomplete.
                # You might want to display an error message or handle this in another appropriate way.
                print("Incomplete data in the selected row.")
                return

            dialog = EditItemDialog(item_id, item_name, item_quantity, item_cost_price, item_selling_price)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                data = dialog.get_data()
                new_item_name = data['name']
                new_quantity = data['quantity']
                new_cost_price = data['cost_price']
                new_selling_price = data['selling_price']

                update_item(item_id, new_item_name, new_quantity, new_cost_price, new_selling_price)

            self.load_data()


    def delete_item(self):
        selected_row = self.table.currentRow()

        if selected_row != -1:
            item_id = self.table.item(selected_row, 0).text()
            item_name = self.table.item(selected_row, 1).text()

            dialog = DeleteItemDialog(item_id, item_name)
            result = dialog.exec_()

            if result == QDialog.Accepted:
                delete_item(item_id)

            self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        data = get_all_items()

        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
        
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
        
            cost_price = float(row_data[3])
            selling_price = float(row_data[4])  # Use the selling price from the database.
            profit = selling_price - cost_price
        
            self.table.setItem(row_number, 4, QTableWidgetItem(f"{selling_price:.2f}"))  # Set the selling price in the Selling Price column
            self.table.setItem(row_number, 5, QTableWidgetItem(f"{profit:.2f}"))  # Set the profit in the Profit column


if __name__ == "__main__":
    app = QApplication(sys.argv)

    inventory_management = InventoryManagement()
    inventory_management.show()

    sys.exit(app.exec_())
