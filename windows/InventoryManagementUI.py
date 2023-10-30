from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt


class InventoryManagementUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)  # To make the window frameless

        self.m_mousePressed = False
        self.m_mousePos = None
        self.m_windowPos = None

        self.layout = QVBoxLayout()
        self.topLayout = QHBoxLayout()  # Top bar layout for close, minimize, maximize buttons

        # Create and style buttons
        self.create_buttons()

        # Title label initialization
        self.titleLabel = QLabel("Inventory")
        title_style = """
        QLabel {
            color: #3A3A3A;
            font-size: 32px;
            font-weight: bold;
        }
        """
        self.titleLabel.setStyleSheet(title_style)
        self.titleLabel.setAlignment(Qt.AlignCenter)  # Center alignment for the label

        # Balance Label Initialization
        self.balanceLabel = QLabel()  # Sample balance text
        self.balanceLabel.setStyleSheet("color: green; font-size: 24px; font-weight: bold;")
        self.balanceLabel.setAlignment(Qt.AlignCenter)  # Center alignment for the label

        # Table Initialization
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Item ID", "Item Name", "Quantity", "Cost Price", "Selling Price", "Profit"])

        # Adding widgets to layout in correct order
        self.layout.addLayout(self.topLayout)
        self.layout.insertWidget(1, self.titleLabel)
        self.layout.addWidget(self.balanceLabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.editButton)
        self.layout.addWidget(self.deleteButton)

        self.setLayout(self.layout)

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

        # Close, Minimize, Maximize buttons with fixed size
        self.btnClose = QPushButton("X")
        self.btnMinimize = QPushButton("-")
        self.btnMaximize = QPushButton("[]")
        self.btnClose.setFixedSize(30, 30)
        self.btnMinimize.setFixedSize(30, 30)
        self.btnMaximize.setFixedSize(30, 30)
        self.btnClose.setStyleSheet(btn_style)
        self.btnMinimize.setStyleSheet(btn_style)
        self.btnMaximize.setStyleSheet(btn_style)
        self.btnClose.clicked.connect(self.close)
        self.btnMinimize.clicked.connect(self.showMinimized)
        self.btnMaximize.clicked.connect(self.toggleMaximize)

        # Positioning buttons on the top left and adding stretch to push them to the left
        self.topLayout.addWidget(self.btnClose)
        self.topLayout.addWidget(self.btnMinimize)
        self.topLayout.addWidget(self.btnMaximize)
        self.topLayout.addStretch(1)

        # Existing buttons with new style
        self.addButton = QPushButton("Add Item")
        self.editButton = QPushButton("Edit Item")
        self.deleteButton = QPushButton("Delete Item")

        # Apply button styles
        self.addButton.setStyleSheet(btn_style)
        self.editButton.setStyleSheet(btn_style)
        self.deleteButton.setStyleSheet(btn_style)

    def toggleMaximize(self):
        if self.windowState() & Qt.WindowMaximized:
            self.showNormal()
        else:
            self.showMaximized()
