from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class DeleteItemDialog(QDialog):
    def __init__(self, item_id, item_name):  # added item_name parameter
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Delete Item")

        # Define the layout
        self.layout = QVBoxLayout()

        # Create the label
        self.label = QLabel(f"Are you sure you want to delete {item_name} with ID {item_id}?")  # use both item_id and item_name

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
