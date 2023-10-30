from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import pyqtSignal
import sys
from functions.balance_functions import get_balance, set_balance  # Import the required function
from dialogs.adjust_balance_dialog import AdjustBalanceDialog

class MainWindow(QMainWindow):
    balance_updated = pyqtSignal()
    
    def __init__(self, inventory_management, sales_management, expense_tracking, profit_calculation):
        super().__init__()

        self.balance_updated.connect(self.update_balance)

        self.m_mousePressed = False
        self.m_mousePos = None
        self.m_windowPos = None

        # Save the window references
        self.inventory_management = inventory_management
        self.sales_management = sales_management
        self.expense_tracking = expense_tracking
        self.profit_calculation = profit_calculation

        # Set window properties
        self.setWindowTitle("Beauty Sales Management System")
        self.setGeometry(100, 100, 400, 600)

        # Set a more modern style
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove traditional title bar for a modern look
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set a light/dark color palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # Create layout and set it to central widget
        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet("background-color: #2A2A2A; border-radius: 15px;")
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Create Balance Label
        self.create_balance_label()

        # Create buttons
        self.create_buttons()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_mousePressed = True
            self.m_mousePos = event.globalPos()
            self.m_windowPos = self.pos()
            event.accept()

    # Mouse move event to move the window as you drag
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.m_mousePressed:
            moveOffset = event.globalPos() - self.m_mousePos
            newWindowPos = self.m_windowPos + moveOffset
            self.move(newWindowPos)
            event.accept()

    # Mouse release event to stop the drag
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_mousePressed = False
            event.accept()

    def create_balance_label(self):
        balance = get_balance()
        self.balanceLabel = QLabel(f"Balance: {balance:.2f} LYD")
        self.balanceLabel.setAlignment(Qt.AlignCenter)
        self.balanceLabel.setFont(QFont("Arial", 24, QFont.Bold))
        self.balanceLabel.setStyleSheet("color: #4CAF50; padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; background-color: #1A1A1A;")
        self.layout.addWidget(self.balanceLabel)

    def create_buttons(self):
        # Style for all buttons
        btn_style = """
        QPushButton {
            color: white;
            font-size: 16px;
            padding: 10px;
            border: 1px solid #555;
            border-radius: 10px;
            background-color: #3A3A3A;
        }
        QPushButton:hover {
            background-color: #4A4A4A;
        }
        QPushButton:pressed {
            background-color: #5A5A5A;
        }
        """

        self.adjustBalanceButton = QPushButton("Adjust Balance")
        self.inventoryButton = QPushButton("Inventory Management")
        self.salesButton = QPushButton("Sales Management")
        self.expenseButton = QPushButton("Expense Tracking")
        self.profitButton = QPushButton("Profit Calculation")

        # Apply button styles
        self.adjustBalanceButton.setStyleSheet(btn_style)
        self.inventoryButton.setStyleSheet(btn_style)
        self.salesButton.setStyleSheet(btn_style)
        self.expenseButton.setStyleSheet(btn_style)
        self.profitButton.setStyleSheet(btn_style)

        # Connect actions and add to layout
        self.adjustBalanceButton.clicked.connect(self.adjust_balance)
        self.layout.addWidget(self.adjustBalanceButton)

        self.layout.addWidget(self.inventoryButton)
        self.layout.addWidget(self.salesButton)
        self.layout.addWidget(self.expenseButton)
        self.layout.addWidget(self.profitButton)

        self.inventoryButton.clicked.connect(self.inventory_management.show)
        self.salesButton.clicked.connect(self.sales_management.show)
        self.expenseButton.clicked.connect(self.expense_tracking.show)
        self.profitButton.clicked.connect(self.profit_calculation.show)

    def update_balance(self):
        balance = get_balance()
        self.balanceLabel.setText(f"Balance: {balance:.2f} LYD")

    def adjust_balance(self):
        dialog = AdjustBalanceDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            new_balance = dialog.get_balance()
            set_balance(new_balance)
            self.update_balance()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Assuming you have these classes imported
    inventory_management = InventoryManagement()
    sales_management = SalesManagement()
    expense_tracking = ExpenseTracking()
    profit_calculation = ProfitCalculation()

    main_window = MainWindow(inventory_management, sales_management, expense_tracking, profit_calculation)
    main_window.show()

    sys.exit(app.exec_())
