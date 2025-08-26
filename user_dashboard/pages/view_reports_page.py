from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

class ViewReportsPage:
    def __init__(self, parent):
        self.parent = parent

    def create_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title_label = QLabel("📋 Past Reports")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Title", "Content", "Status"])
        layout.addWidget(self.table)

        return widget
