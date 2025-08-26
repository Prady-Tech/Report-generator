from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class HeaderComponent:
    def __init__(self, parent, username):
        self.parent = parent
        self.username = username

    def create_header(self):
        header = QWidget()
        header.setFixedHeight(60)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)

        label = QLabel(f"Welcome, {self.username}")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label)
        layout.addStretch()

        return header
