from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self, inventory_management, sales_management, expense_tracking, profit_calculation):
        super().__init__()

        # Save the window references
        self.inventory_management = inventory_management
        self.sales_management = sales_management
        self.expense_tracking = expense_tracking
        self.profit_calculation = profit_calculation

        # Set window properties
        self.setWindowTitle("Beauty Sales Management System")
        self.setGeometry(100, 100, 400, 600)

        # Create layout and set it to central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        self.inventoryButton = QPushButton("Inventory Management")
        self.salesButton = QPushButton("Sales Management")
        self.expenseButton = QPushButton("Expense Tracking")
        self.profitButton = QPushButton("Profit Calculation")

        # Add buttons to layout
        self.layout.addWidget(self.inventoryButton)
        self.layout.addWidget(self.salesButton)
        self.layout.addWidget(self.expenseButton)
        self.layout.addWidget(self.profitButton)

        # Connect buttons to the windows
        self.inventoryButton.clicked.connect(self.inventory_management.show)
        self.salesButton.clicked.connect(self.sales_management.show)
        self.expenseButton.clicked.connect(self.expense_tracking.show)
        self.profitButton.clicked.connect(self.profit_calculation.show)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the windows
    inventory_management = InventoryManagement()
    sales_management = SalesManagement()
    expense_tracking = ExpenseTracking()
    profit_calculation = ProfitCalculation()

    # Create and show main window
    main_window = MainWindow(inventory_management, sales_management, expense_tracking, profit_calculation)
    main_window.show()

    sys.exit(app.exec_())
