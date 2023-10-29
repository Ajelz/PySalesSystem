from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QComboBox
from functions.sales_functions import get_all_inventory_items


class AddSaleDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Add Sale")

        # Define the layout
        self.layout = QVBoxLayout()

        # Create the labels, line edits, and combo box
        self.itemLabel = QLabel("Product Name:")
        self.itemComboBox = QComboBox()
        
        self.quantityLabel = QLabel("Quantity Sold:")
        self.quantityLineEdit = QLineEdit()

        # Load product names into the combo box
        self.load_product_names()

        # Add labels, combo box, and line edits to layout
        self.layout.addWidget(self.itemLabel)
        self.layout.addWidget(self.itemComboBox)
        self.layout.addWidget(self.quantityLabel)
        self.layout.addWidget(self.quantityLineEdit)

        # Create the button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add button box to layout
        self.layout.addWidget(self.buttonBox)

        # Set the layout
        self.setLayout(self.layout)

    def load_product_names(self):
        """Populate the combo box with product names."""
        inventory_items = get_all_inventory_items()
        for item in inventory_items:
            item_id, product_name, _ = item
            self.itemComboBox.addItem(product_name, item_id)

    def get_input_values(self):
        """Retrieve the selected product and entered quantity."""
        return {
            "item_id": self.itemComboBox.currentData(),
            "quantity": self.quantityLineEdit.text()
        }
