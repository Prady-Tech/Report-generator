# admin_pages.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,
    QListWidget, QTableWidget, QFrame, QMessageBox
)
from PySide6.QtCore import Qt


class AddUserPage:
    def __init__(self, parent):
        self.parent = parent

    def create_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        # Card Frame
        card = QFrame()
        card.setFixedSize(400, 350)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 15px;
                padding: 20px;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #374151;
                border: 1px solid #4b5563;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                color: #e2e8f0;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignTop)
        card_layout.setSpacing(15)

        # Title
        title = QLabel("➕ Add User")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Input fields
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Full Name")
        card_layout.addWidget(self.input_name)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        card_layout.addWidget(self.input_email)

        self.input_role = QComboBox()
        self.input_role.addItems(["Admin", "Editor", "Viewer"])
        card_layout.addWidget(self.input_role)

        # Submit button
        submit_btn = QPushButton("Add User")
        submit_btn.clicked.connect(self.add_user)
        card_layout.addWidget(submit_btn)

        layout.addWidget(card, alignment=Qt.AlignCenter)
        return page

    def add_user(self):
        name = self.input_name.text().strip()
        email = self.input_email.text().strip()
        role = self.input_role.currentText()

        if not name or not email:
            QMessageBox.warning(self.parent, "Input Error", "Name and email are required.")
            return

        try:
            success = self.parent.data_manager.add_user_to_db(name, email, role)
            if not success:
                QMessageBox.warning(self.parent, "Duplicate", f"User '{name}' already exists.")
                return
        except Exception as e:
            QMessageBox.critical(self.parent, "Database Error", str(e))
            return

        self.parent.refresh_users()
        QMessageBox.information(self.parent, "Success", f"User '{name}' added as {role}.")

        self.input_name.clear()
        self.input_email.clear()
        self.input_role.setCurrentIndex(0)


class DeleteUsersPage:
    def __init__(self, parent):
        self.parent = parent

    def create_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        # Card frame
        card = QFrame()
        card.setFixedSize(400, 350)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 15px;
                padding: 20px;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 16px;
                font-weight: bold;
            }
            QListWidget {
                background-color: #374151;
                border: 1px solid #4b5563;
                border-radius: 8px;
                color: #e2e8f0;
                font-size: 14px;
                padding: 5px;
            }
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
            QPushButton:pressed {
                background-color: #b91c1c;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignTop)
        card_layout.setSpacing(15)

        # Title
        title = QLabel("🗑️ Delete Users")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # User list
        self.user_list_widget = QListWidget()
        card_layout.addWidget(self.user_list_widget)

        # Delete button
        delete_btn = QPushButton("Delete Selected User")
        delete_btn.clicked.connect(self.delete_user)
        card_layout.addWidget(delete_btn)

        layout.addWidget(card, alignment=Qt.AlignCenter)
        return page

    def delete_user(self):
        selected_items = self.user_list_widget.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            user_name = item.text()
            try:
                self.parent.data_manager.delete_user_from_db(user_name)
            except Exception as e:
                QMessageBox.critical(self.parent, "Database Error", str(e))
                return

        self.parent.refresh_users()
        QMessageBox.information(self.parent, "Deleted", f"User '{user_name}' deleted successfully.")


class ReportsPage:
    def __init__(self, parent):
        self.parent = parent

    def create_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        # Card frame
        card = QFrame()
        card.setFixedSize(600, 400)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 15px;
                padding: 20px;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 16px;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #374151;
                border: 1px solid #4b5563;
                border-radius: 8px;
                color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3b82f6;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        card_layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("📊 User Reports")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Table
        self.reports_table = QTableWidget(0, 3)
        self.reports_table.setHorizontalHeaderLabels(["User", "Report", "Status"])
        card_layout.addWidget(self.reports_table)

        layout.addWidget(card, alignment=Qt.AlignCenter)

        self.parent.reports_table = self.reports_table
        return page


class ProfilesPage:
    def __init__(self, parent):
        self.parent = parent

    def create_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        # Card frame
        card = QFrame()
        card.setFixedSize(600, 400)
        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-radius: 15px;
                padding: 20px;
            }
            QLabel {
                color: #e2e8f0;
                font-size: 16px;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #374151;
                border: 1px solid #4b5563;
                border-radius: 8px;
                color: #e2e8f0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3b82f6;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        card_layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("👤 User Profiles")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Table
        self.profiles_table = QTableWidget(0, 3)
        self.profiles_table.setHorizontalHeaderLabels(["Name", "Email", "Role"])
        card_layout.addWidget(self.profiles_table)

        layout.addWidget(card, alignment=Qt.AlignCenter)

        self.parent.profiles_table = self.profiles_table
        return page
