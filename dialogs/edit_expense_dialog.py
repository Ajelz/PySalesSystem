from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox

class EditExpenseDialog(QDialog):
    def __init__(self, current_type, current_amount):
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Edit Expense")

        # Define the layout
        self.layout = QVBoxLayout()

        # Create the labels and line edits
        self.typeLabel = QLabel("Expense Type:")
        self.typeEdit = QLineEdit()
        self.amountLabel = QLabel("Expense Amount:")
        self.amountEdit = QLineEdit()

        # Set the current values
        self.typeEdit.setText(current_type)
        self.amountEdit.setText(str(current_amount))

        # Add widgets to layout
        self.layout.addWidget(self.typeLabel)
        self.layout.addWidget(self.typeEdit)
        self.layout.addWidget(self.amountLabel)
        self.layout.addWidget(self.amountEdit)

        # Create the button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add button box to layout
        self.layout.addWidget(self.buttonBox)

        # Set the layout
        self.setLayout(self.layout)

    def get_values(self):
        # This function is used to get the values entered by the user
        return self.typeEdit.text(), self.amountEdit.text()
