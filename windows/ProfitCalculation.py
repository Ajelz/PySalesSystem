from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from functions.profit_functions import calculate_profit
import sys

class ProfitCalculation(QWidget):
    def __init__(self):
        super().__init__()

        # Define the window properties
        self.setWindowTitle("Profit Calculation")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)  # To make the window frameless

        self.m_mousePressed = False
        self.m_mousePos = None
        self.m_windowPos = None

        # Define layout
        self.layout = QVBoxLayout()
        self.topLayout = QHBoxLayout()  # Top bar layout for close, minimize buttons

        # Create and style buttons
        self.create_buttons()

        # Title label initialization
        self.titleLabel = QLabel("Profit")
        title_style = """
        QLabel {
            color: #3A3A3A;
            font-size: 24px;
            font-weight: bold;
        }
        """
        self.titleLabel.setStyleSheet(title_style)
        self.titleLabel.setAlignment(Qt.AlignCenter)  # Center alignment for the label

        # Create the label for profit display
        self.profitLabel = QLabel()
        self.profitLabel.setAlignment(Qt.AlignCenter)
        self.profitLabel.setStyleSheet("color: green; font-size: 24px; font-weight: bold;")  # New styling for profitLabel

        # Add widgets to layout in correct order
        self.layout.addLayout(self.topLayout)
        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.profitLabel)
        self.layout.addWidget(self.refreshButton)

        # Set the layout
        self.setLayout(self.layout)
        self.refresh_profit()

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

    def create_buttons(self):
        # Button style
        btn_style = """
        QPushButton {
            color: white;
            font-size: 16px;
            padding: 5px;
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

        # Close, Minimize buttons with fixed size
        self.btnClose = QPushButton("X")
        self.btnMinimize = QPushButton("-")
        self.btnClose.setFixedSize(30, 30)
        self.btnMinimize.setFixedSize(30, 30)
        self.btnClose.setStyleSheet(btn_style)
        self.btnMinimize.setStyleSheet(btn_style)
        self.btnClose.clicked.connect(self.close)
        self.btnMinimize.clicked.connect(self.showMinimized)

        # Positioning buttons on the top left and adding stretch to push them to the left
        self.topLayout.addWidget(self.btnClose)
        self.topLayout.addWidget(self.btnMinimize)
        self.topLayout.addStretch(1)

        # Existing button with new style
        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.setStyleSheet(btn_style)
        self.refreshButton.clicked.connect(self.refresh_profit)

    def refresh_profit(self):
        profit = calculate_profit()
        self.profitLabel.setText(f"Current Profit: {profit:.2f} LYD")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    profit_calculation = ProfitCalculation()
    profit_calculation.show()

    sys.exit(app.exec_())
