from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt

class CreateReportPage:
    def __init__(self, parent):
        self.parent = parent

    def create_page(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title_label = QLabel("📄 Create New Report")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Report Title")
        layout.addWidget(self.title_input)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Report Content")
        layout.addWidget(self.content_input)

        button_layout = QHBoxLayout()
        submit_btn = QPushButton("Submit Report")
        submit_btn.clicked.connect(self.submit_report)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(submit_btn)
        button_layout.addWidget(clear_btn)
        layout.addLayout(button_layout)

        return widget

    def submit_report(self):
        title = self.title_input.text()
        content = self.content_input.toPlainText()
        if not title or not content:
            QMessageBox.warning(self.parent, "Incomplete Report", "Please enter both title and content.")
            return
        QMessageBox.information(self.parent, "Report Submitted", f"Report '{title}' submitted successfully!")
        self.clear_form()

    def clear_form(self):
        self.title_input.clear()
        self.content_input.clear()
