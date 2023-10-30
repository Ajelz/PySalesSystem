from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout

class AdjustBalanceDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adjust Balance")
        self.layout = QVBoxLayout()

        self.infoLabel = QLabel("Enter the new balance:")
        self.balanceLineEdit = QLineEdit()

        self.buttonLayout = QHBoxLayout()
        self.applyButton = QPushButton("Apply")
        self.cancelButton = QPushButton("Cancel")

        self.applyButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

        self.buttonLayout.addWidget(self.applyButton)
        self.buttonLayout.addWidget(self.cancelButton)

        self.layout.addWidget(self.infoLabel)
        self.layout.addWidget(self.balanceLineEdit)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)

    def get_balance(self):
        return float(self.balanceLineEdit.text())
