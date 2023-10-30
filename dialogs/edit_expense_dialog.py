from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QDialogButtonBox

class EditExpenseDialog(QDialog):
    def __init__(self, expense_id, current_type, current_amount):
        super().__init__()

        # Store expense_id for later use
        self.expense_id = expense_id

        # Define the window properties
        self.setWindowTitle("Edit Expense")

        # Define the form layout
        self.layout = QFormLayout()

        # Create the form fields and pre-fill them with data
        self.typeField = QLineEdit(current_type)
        self.amountField = QLineEdit(str(current_amount))

        # Add form fields to layout
        self.layout.addRow(QLabel("Expense Type"), self.typeField)
        self.layout.addRow(QLabel("Expense Amount"), self.amountField)

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
            'expense_id': self.expense_id,
            'type': self.typeField.text(),
            'amount': float(self.amountField.text())
        }
