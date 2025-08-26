from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QTableWidgetItem
from admin.header_component import HeaderComponent
from admin.sidebar_component import SidebarComponent
from admin.admin_pages import AddUserPage, ReportsPage, ProfilesPage, DeleteUsersPage
from admin.data_manager import DataManager

class AdminDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.data_manager = DataManager()
        self.users_data = []

        self.init_ui()
        self.refresh_users()  # Load users at startup

    def init_ui(self):
        """Initialize dashboard layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        self.header = HeaderComponent(self)
        layout.addWidget(self.header.create_header())

        # Body
        body_layout = QHBoxLayout()
        layout.addLayout(body_layout)

        # Sidebar
        sidebar_component = SidebarComponent(self)
        self.sidebar_widget = sidebar_component.create_sidebar()
        body_layout.addWidget(self.sidebar_widget)

        # Store button references
        self.btn_dashboard = sidebar_component.btn_dashboard
        self.btn_add_user = sidebar_component.btn_add_user
        self.btn_view_reports = sidebar_component.btn_view_reports
        self.btn_view_profiles = sidebar_component.btn_view_profiles
        self.btn_delete_users = sidebar_component.btn_delete_users

        # Connect signals
        self.btn_dashboard.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_add_user.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_view_reports.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_view_profiles.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_delete_users.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        # Main content stack
        self.stack = QStackedWidget()
        body_layout.addWidget(self.stack)

        # Pages
        self.add_user_page = AddUserPage(self)
        self.reports_page = ReportsPage(self)
        self.profiles_page = ProfilesPage(self)
        self.delete_users_page = DeleteUsersPage(self)

        self.stack.addWidget(self.add_user_page.create_page())      # index 0
        self.stack.addWidget(self.reports_page.create_page())       # index 1
        self.stack.addWidget(self.profiles_page.create_page())      # index 2
        self.stack.addWidget(self.delete_users_page.create_page())  # index 3

    # ------------------------ USER DATA -------------------------
    def refresh_users(self):
        """Reload users from database and update UI"""
        self.users_data = self.data_manager.load_users_from_db()
        self.load_users(self.users_data)
        self.load_user_list(self.users_data)

    def load_users(self, users):
        """Update users in the profiles table"""
        if hasattr(self, "profiles_table"):
            self.profiles_table.setRowCount(0)
            for user in users:
                row = self.profiles_table.rowCount()
                self.profiles_table.insertRow(row)
                self.profiles_table.setItem(row, 0, QTableWidgetItem(user["name"]))
                self.profiles_table.setItem(row, 1, QTableWidgetItem(user["email"]))
                self.profiles_table.setItem(row, 2, QTableWidgetItem(user["role"]))

    def load_user_list(self, users):
        """Update users in the delete-users list"""
        if hasattr(self, "user_list_widget"):
            self.user_list_widget.clear()
            for user in users:
                self.user_list_widget.addItem(user["name"])
