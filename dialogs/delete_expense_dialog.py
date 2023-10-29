from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox

class DeleteExpenseDialog(QDialog):
    def __init__(self, expense_type, expense_amount):
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Delete Expense")

        # Define the layout
        self.layout = QVBoxLayout()

        # Create the labels and line edits
        self.warningLabel = QLabel(f"Are you sure you want to delete the expense '{expense_type}' of amount {expense_amount}? This action cannot be undone.")

        # Add widgets to layout
        self.layout.addWidget(self.warningLabel)

        # Create the button box
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # Connect the signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Add button box to layout
        self.layout.addWidget(self.buttonBox)

        # Set the layout
        self.setLayout(self.layout)
