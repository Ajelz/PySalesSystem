from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class DeleteSaleDialog(QDialog):
    def __init__(self, sale_id):  # added item_id parameter
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Delete Sale")

        # Define the layout
        self.layout = QVBoxLayout()

        # Create the label
        self.label = QLabel(f"Are you sure you want to delete sale with ID {sale_id}?")

        # Add label to layout
        self.layout.addWidget(self.label)

        # Create the button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add button box to layout
        self.layout.addWidget(self.buttonBox)

        # Set the layout
        self.setLayout(self.layout)
