from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from db import verify_user, init_db


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fortress Report - Login")
        self.setModal(True)  # modal blocks until closed
        self.setMinimumSize(400, 400)

        self.role = None  # Will store user role

        # ---- Center Frame (Card style) ----
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)

        frame = QFrame()
        frame.setFixedSize(400, 400)
        frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignTop)

        # ---- Title ----
        label_title = QLabel("Fortress Report")
        label_title.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        label_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_title)

        label_subtitle = QLabel("Please login to continue")
        label_subtitle.setStyleSheet("font-size: 14px; color: lightgray;")
        label_subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_subtitle)

        # ---- Username ----
        self.entry_user = QLineEdit()
        self.entry_user.setPlaceholderText("Username")
        self.entry_user.setFixedHeight(40)
        self.entry_user.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 14px;")
        layout.addWidget(self.entry_user)

        # ---- Password ----
        self.entry_pass = QLineEdit()
        self.entry_pass.setPlaceholderText("Password")
        self.entry_pass.setEchoMode(QLineEdit.Password)
        self.entry_pass.setFixedHeight(40)
        self.entry_pass.setStyleSheet("border-radius: 10px; padding: 5px; font-size: 14px;")
        layout.addWidget(self.entry_pass)

        # ---- Login Button ----
        btn_login = QPushButton("Login")
        btn_login.setFixedHeight(45)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        btn_login.clicked.connect(self.attempt_login)
        layout.addWidget(btn_login)

        # ---- Footer ----
        footer = QLabel("© 2025 Fortress Systems")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 10px; color: gray;")
        layout.addWidget(footer)

        outer_layout.addWidget(frame, alignment=Qt.AlignCenter)

    def attempt_login(self):
        username = self.entry_user.text()
        password = self.entry_pass.text()
        valid, role = verify_user(username, password)
        if valid:
            QMessageBox.information(self, "Login Successful", f"Welcome {username} ({role})")
            self.role = role
            self.accept()  # closes dialog and returns exec_()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")


def run_login():
    """Show login dialog and return role."""
    init_db()
    dialog = LoginDialog()
    dialog.exec()  # blocks until dialog closed
    return dialog.role
