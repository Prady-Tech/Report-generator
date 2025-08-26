# user_dashboard/user_dashboard.py

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from .components.sidebar_component import SidebarComponent
from .pages.create_reports_page import CreateReportPage
from .pages.view_reports_page import ViewReportsPage


class UserDashboard(QMainWindow):
    def __init__(self, username="User"):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"User Dashboard - {self.username}")
        self.setGeometry(200, 200, 900, 600)

        # Main container
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QHBoxLayout(container)

        # Sidebar (keep the component instance so we can access its buttons)
        self.sidebar_component = SidebarComponent(self)
        sidebar_frame = self.sidebar_component.create_sidebar()
        main_layout.addWidget(sidebar_frame)

        # Stacked pages
        self.pages = QStackedWidget()
        self.create_page = CreateReportPage(self).create_page()
        self.view_page = ViewReportsPage(self).create_page()
        self.pages.addWidget(self.create_page)
        self.pages.addWidget(self.view_page)
        main_layout.addWidget(self.pages)

        # Connect sidebar buttons using the component (not the QFrame)
        self.sidebar_component.btn_create_report.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.create_page)
        )
        self.sidebar_component.btn_view_reports.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.view_page)
        )

        # start on create page
        self.pages.setCurrentWidget(self.create_page)
