from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt


class HeaderComponent:
    def __init__(self, parent):
        self.parent = parent  # parent is your dashboard (AdminDashboard/UserDashboard)

    def create_header(self):
        """Create the header widget"""
        header = QWidget()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                border-bottom: 1px solid #334155;
            }
            QLineEdit {
                background-color: #374151;
                border: 1px solid #4b5563;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                color: #e2e8f0;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 14px;
                font-weight: 500;
            }
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search users, reports...")
        self.search_input.setFixedWidth(300)
        header_layout.addWidget(self.search_input)

        header_layout.addStretch()

        # Notifications
        self.label_notification = QLabel("🔔")
        self.label_notification.setFixedSize(30, 30)
        self.label_notification.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.label_notification)

        # User info
        username = getattr(self.parent, "username", "Guest")
        self.label_user = QLabel(f"👤 {username}")
        self.label_user.setStyleSheet("QLabel { margin-left: 15px; }")
        header_layout.addWidget(self.label_user)

        return header
