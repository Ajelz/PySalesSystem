from PyQt5.QtWidgets import QApplication
from windows import MainWindow, InventoryManagement, SalesManagement, ExpenseTracking, ProfitCalculation
import sys

def main():
    # Create the application
    app = QApplication(sys.argv)

    # Create the windows
    inventory_management = InventoryManagement()
    sales_management = SalesManagement()
    expense_tracking = ExpenseTracking()
    profit_calculation = ProfitCalculation()

    # Connect the sale_updated_signal from SalesManagement to the load_data of InventoryManagement
    sales_management.sale_updated_signal.connect(inventory_management.load_data)
    
    # Create the main window
    main_window = MainWindow(inventory_management, sales_management, expense_tracking, profit_calculation)

    # Link the main window to the inventory_management
    inventory_management.main_window = main_window
    # Link the main window to the inventory_management
    SalesManagement.main_window = main_window
    # Link the main window to the inventory_management
    ExpenseTracking.main_window = main_window

    # Show the main window
    main_window.show()

    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
