from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QDialogButtonBox

class AddItemDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Add New Item")

        # Define the form layout
        self.layout = QFormLayout()

        # Create the form fields
        self.nameField = QLineEdit()
        self.quantityField = QLineEdit()
        self.costPriceField = QLineEdit()
        self.sellingPriceField = QLineEdit()  # New field for selling price

        # Add form fields to layout
        self.layout.addRow(QLabel("Item Name"), self.nameField)
        self.layout.addRow(QLabel("Quantity"), self.quantityField)
        self.layout.addRow(QLabel("Cost Price"), self.costPriceField)
        self.layout.addRow(QLabel("Selling Price"), self.sellingPriceField)  # Added to layout

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
            'selling_price': float(self.sellingPriceField.text())  # Added selling price
        }
