from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QDialogButtonBox

class EditItemDialog(QDialog):
    def __init__(self, item_id, item_name, item_quantity, item_cost_price, item_selling_price):  # Include selling price as an argument
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Edit Item")

        # Define the form layout
        self.layout = QFormLayout()

        # Create the form fields and pre-fill them with item data
        self.nameField = QLineEdit(item_name)
        self.quantityField = QLineEdit(str(item_quantity))
        self.costPriceField = QLineEdit(str(item_cost_price))
        self.sellingPriceField = QLineEdit(str(item_selling_price))  # New field for selling price

        # Add form fields to layout
        self.layout.addRow(QLabel("Item Name"), self.nameField)
        self.layout.addRow(QLabel("Quantity"), self.quantityField)
        self.layout.addRow(QLabel("Cost Price"), self.costPriceField)
        self.layout.addRow(QLabel("Selling Price"), self.sellingPriceField)  # New row for selling price

        # Create the button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add button box to layout
        self.layout.addRow(self.buttonBox)

        # Set the layout
        self.setLayout(self.layout)

    def get_data(self):
        return {
            'name': self.nameField.text(),
            'quantity': int(self.quantityField.text()),
            'cost_price': float(self.costPriceField.text()),
            'selling_price': float(self.sellingPriceField.text())  # Return selling price
        }
