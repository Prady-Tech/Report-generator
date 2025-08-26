from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt

class SidebarComponent:
    def __init__(self, parent):
        self.parent = parent
        self.btn_create_report = None
        self.btn_view_reports = None

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1e293b; 
                border-right: 1px solid #334155;
            }
            QPushButton {
                background-color: transparent;
                color: #e2e8f0;
                border: none;
                padding: 12px 16px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
                border-radius: 6px;
                margin: 2px 0;
            }
            QPushButton:hover {
                background-color: #334155;
            }
            QPushButton:pressed {
                background-color: #3b82f6;
            }
        """)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(8)

        # Title
        title = QLabel("Fortress Report")
        title.setStyleSheet("color: #3b82f6; font-weight: bold; font-size: 18px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(20)

        # Buttons
        self.btn_create_report = QPushButton("📄 Create Report")
        self.btn_view_reports = QPushButton("📋 View Past Reports")

        # Expose buttons to parent for navigation
        self.parent.btn_create_report = self.btn_create_report
        self.parent.btn_view_reports = self.btn_view_reports

        layout.addWidget(self.btn_create_report)
        layout.addWidget(self.btn_view_reports)
        layout.addStretch()

        return sidebar
