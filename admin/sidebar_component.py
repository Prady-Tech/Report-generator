from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt

class SidebarComponent:
    def __init__(self, parent):
        self.parent = parent

    def create_sidebar(self):
        """Create the sidebar widget"""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
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
                margin: 2px 8px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
            QPushButton:pressed {
                background-color: #3b82f6;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 20, 16, 20)
        sidebar_layout.setSpacing(8)

        # Title
        title = QLabel("Fortress Report")
        title.setStyleSheet("""
            QLabel {
                color: #3b82f6;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 0;
            }
        """)
        sidebar_layout.addWidget(title)

        # Buttons
        self.btn_dashboard = QPushButton("📊 Dashboard")
        self.btn_add_user = QPushButton("➕ Add User")
        self.btn_view_reports = QPushButton("📋 View Reports")
        self.btn_view_profiles = QPushButton("👤 View Profiles")
        self.btn_delete_users = QPushButton("🗑️ Delete Users")

        for btn in [self.btn_dashboard, self.btn_add_user, self.btn_view_reports,
                    self.btn_view_profiles, self.btn_delete_users]:
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        return sidebar
