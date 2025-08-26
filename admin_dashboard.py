import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QMessageBox, QFrame, QComboBox
)
from PySide6.QtCore import Qt, QTimer


class AdminDashboard(QMainWindow):
    def __init__(self, username="Admin"):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setGeometry(100, 100, 1200, 700)
        self.username = username

        # --- Mock data (now dicts with name, email, role) ---
        self.reports_data = [
            {"user": "Alice", "report": "Monthly Sales", "status": "Approved"},
            {"user": "Bob", "report": "Weekly Check-in", "status": "Pending"},
            {"user": "Charlie", "report": "Annual Review", "status": "Rejected"},
        ]
        self.users_data = [
            {"name": "Alice", "email": "alice@example.com", "role": "Admin"},
            {"name": "Bob", "email": "bob@example.com", "role": "Editor"},
            {"name": "Charlie", "email": "charlie@example.com", "role": "Viewer"},
            {"name": "David", "email": "david@example.com", "role": "Editor"},
        ]

        # ------------------ Main container ------------------
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ------------------ Sidebar ------------------
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setFixedWidth(260)
        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        sidebar_layout.setContentsMargins(20, 18, 10, 10)
        sidebar_layout.setSpacing(8)

        logo_label = QLabel("⚪ DashboardKit")
        logo_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        logo_container = QWidget()
        logo_container.setStyleSheet("background-color: #1f2937; border-radius: 6px;")
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(12, 10, 12, 10)
        logo_layout.addWidget(logo_label)
        sidebar_layout.addWidget(logo_container)
        sidebar_layout.addSpacing(12)

        # NAVIGATION
        nav_label = QLabel("NAVIGATION")
        nav_label.setStyleSheet("font-size: 11px; color: #9aa4b2; font-weight: 700;")
        sidebar_layout.addWidget(nav_label)

        self.btn_dashboard = QPushButton("🏠  Dashboard")
        self.btn_dashboard.setFixedHeight(36)
        self._style_sidebar_btn(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_dashboard)

        sidebar_layout.addSpacing(8)

        # ELEMENTS
        elements_label = QLabel("ELEMENTS")
        elements_label.setStyleSheet("font-size: 11px; color: #9aa4b2; font-weight: 700; margin-top:8px;")
        sidebar_layout.addWidget(elements_label)

        self.btn_add_user = QPushButton("➕  Add User")
        self._style_sidebar_btn(self.btn_add_user)
        sidebar_layout.addWidget(self.btn_add_user)

        self.btn_view_reports = QPushButton("📊  View Reports")
        self._style_sidebar_btn(self.btn_view_reports)
        sidebar_layout.addWidget(self.btn_view_reports)

        # PAGES
        pages_label = QLabel("PAGES")
        pages_label.setStyleSheet("font-size: 11px; color: #9aa4b2; font-weight: 700; margin-top:12px;")
        sidebar_layout.addWidget(pages_label)

        self.btn_view_profiles = QPushButton("👤  View Profiles")
        self._style_sidebar_btn(self.btn_view_profiles)
        sidebar_layout.addWidget(self.btn_view_profiles)

        self.btn_delete_users = QPushButton("🗑️  Delete Users")
        self._style_sidebar_btn(self.btn_delete_users)
        sidebar_layout.addWidget(self.btn_delete_users)

        sidebar_layout.addStretch()
        main_layout.addWidget(self.sidebar_widget)

        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setLineWidth(1)
        separator.setStyleSheet("color: #2b2f36;")
        main_layout.addWidget(separator)

        # ------------------ Right: Header + Main Area ------------------
        right_container = QWidget()
        right_vlayout = QVBoxLayout(right_container)
        right_vlayout.setContentsMargins(12, 12, 12, 12)
        right_vlayout.setSpacing(10)

        # Header with search + user info
        top_header = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search reports/users...")
        self.search_input.setFixedHeight(36)
        self.search_input.textChanged.connect(self.filter_items)
        self.search_input.setStyleSheet("border-radius: 8px; padding-left: 10px;")
        top_header.addWidget(self.search_input)
        top_header.addStretch()
        self.label_notification = QLabel("🔔")
        self.label_notification.setStyleSheet("font-size: 18px;")
        self.label_notification.setToolTip("No new notifications")
        top_header.addWidget(self.label_notification)
        self.label_user = QLabel(f"Welcome, {self.username}")
        self.label_user.setStyleSheet("font-size: 13px; font-weight: 600;")
        top_header.addWidget(self.label_user)
        right_vlayout.addLayout(top_header)

        # Stacked pages
        self.main_area = QStackedWidget()
        self.page_add_user = self.create_add_user_page()
        self.page_reports = self.create_reports_page()
        self.page_profiles = self.create_profiles_page()
        self.page_delete = self.create_delete_page()
        for page in [self.page_add_user, self.page_reports, self.page_profiles, self.page_delete]:
            self.main_area.addWidget(page)
        right_vlayout.addWidget(self.main_area)
        main_layout.addWidget(right_container)

        # Button navigation
        self.btn_dashboard.clicked.connect(lambda: self.main_area.setCurrentIndex(1))
        self.btn_add_user.clicked.connect(lambda: self.main_area.setCurrentIndex(0))
        self.btn_view_reports.clicked.connect(lambda: self.main_area.setCurrentIndex(1))
        self.btn_view_profiles.clicked.connect(lambda: self.main_area.setCurrentIndex(2))
        self.btn_delete_users.clicked.connect(lambda: self.main_area.setCurrentIndex(3))

        # Notifications mock
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.mock_new_report)
        self.notification_timer.start(10000)
        self.last_report_count = len(self.reports_data)

    # ---------------- Sidebar helper ----------------
    def _style_sidebar_btn(self, btn: QPushButton):
        btn.setFixedHeight(36)
        btn.setStyleSheet("text-align: left; padding-left: 12px; border: none; color: #e5e7eb; font-size: 13px;")

    # ---------------- Pages ----------------
    def create_add_user_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("➕ Add User")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Enter full name")
        layout.addWidget(self.input_name)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Enter email")
        layout.addWidget(self.input_email)

        self.input_role = QComboBox()
        self.input_role.addItems(["Admin", "Editor", "Viewer"])
        layout.addWidget(self.input_role)

        submit_btn = QPushButton("Add User")
        submit_btn.clicked.connect(self.add_user)
        layout.addWidget(submit_btn)

        layout.addStretch()
        return widget

    def create_reports_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("📊 User Reports")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.reports_table = QTableWidget(0, 3)
        self.reports_table.setHorizontalHeaderLabels(["User", "Report", "Status"])
        layout.addWidget(self.reports_table)
        self.load_reports(self.reports_data)
        return widget

    def create_profiles_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("👤 User Profiles")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.profiles_table = QTableWidget(0, 3)
        self.profiles_table.setHorizontalHeaderLabels(["Name", "Email", "Role"])
        layout.addWidget(self.profiles_table)
        self.load_users(self.users_data)
        return widget

    def create_delete_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("🗑️ Delete Users")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.user_list_widget = QListWidget()
        self.load_user_list(self.users_data)
        delete_btn = QPushButton("Delete Selected User")
        delete_btn.clicked.connect(self.delete_user)
        layout.addWidget(self.user_list_widget)
        layout.addWidget(delete_btn)
        return widget

    # ---------------- Helpers ----------------
    def load_reports(self, reports):
        self.reports_table.setRowCount(0)
        for report in reports:
            row = self.reports_table.rowCount()
            self.reports_table.insertRow(row)
            self.reports_table.setItem(row, 0, QTableWidgetItem(report["user"]))
            self.reports_table.setItem(row, 1, QTableWidgetItem(report["report"]))
            self.reports_table.setItem(row, 2, QTableWidgetItem(report["status"]))

    def load_users(self, users):
        self.profiles_table.setRowCount(0)
        for user in users:
            row = self.profiles_table.rowCount()
            self.profiles_table.insertRow(row)
            self.profiles_table.setItem(row, 0, QTableWidgetItem(user["name"]))
            self.profiles_table.setItem(row, 1, QTableWidgetItem(user["email"]))
            self.profiles_table.setItem(row, 2, QTableWidgetItem(user["role"]))

    def load_user_list(self, users):
        self.user_list_widget.clear()
        for user in users:
            self.user_list_widget.addItem(QListWidgetItem(user["name"]))

    def add_user(self):
        name = self.input_name.text().strip()
        email = self.input_email.text().strip()
        role = self.input_role.currentText()

        if not name or not email:
            QMessageBox.warning(self, "Input Error", "Name and email are required.")
            return

        if any(u["name"] == name for u in self.users_data):
            QMessageBox.warning(self, "Duplicate", f"User '{name}' already exists.")
            return

        new_user = {"name": name, "email": email, "role": role}
        self.users_data.append(new_user)
        self.load_users(self.users_data)
        self.load_user_list(self.users_data)

        QMessageBox.information(self, "Success", f"User '{name}' added as {role}.")
        self.input_name.clear()
        self.input_email.clear()
        self.input_role.setCurrentIndex(0)

    def delete_user(self):
        selected_items = self.user_list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            user_name = item.text()
            self.users_data = [u for u in self.users_data if u["name"] != user_name]
            self.user_list_widget.takeItem(self.user_list_widget.row(item))
        self.load_users(self.users_data)
        QMessageBox.information(self, "Deleted", f"User '{user_name}' deleted successfully.")

    # ---------------- Actions ----------------
    def filter_items(self, text):
        text = text.lower()
        filtered_reports = [r for r in self.reports_data if text in r["user"].lower() or text in r["report"].lower()]
        self.load_reports(filtered_reports)

        filtered_users = [u for u in self.users_data if text in u["name"].lower() or text in u["email"].lower()]
        self.load_users(filtered_users)

    def mock_new_report(self):
        new_report = {"user": "NewUser", "report": "Monthly Summary", "status": "Pending"}
        self.reports_data.append(new_report)
        self.load_reports(self.reports_data)
        self.label_notification.setText("🔔 •")
        self.label_notification.setToolTip(f"New report submitted by {new_report['user']}")


# ---------------- Wrapper ----------------
def run_admin_dashboard(username="Admin"):
    app = QApplication(sys.argv)
    window = AdminDashboard(username=username)
    window.show()
    sys.exit(app.exec())
