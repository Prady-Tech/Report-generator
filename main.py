import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from auth import run_login
from database import init_db
from admin_dashboard import AdminDashboard
from user_dashboard.user_dashboard import UserDashboard


def main():
    """Entry point for the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Fortress Report")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Fortress Systems")

    try:
        print("Initializing database...")
        init_db()
        print("Database initialized successfully.")

        print("Starting login process...")
        role = run_login()

        if not role:
            print("Login cancelled or failed.")
            return

        print(f"Login successful. Role: {role}")

        # Launch appropriate dashboard
        if role == "admin":
            print("Loading admin dashboard...")
            window = AdminDashboard(username="admin")
        else:
            print("Loading user dashboard...")
            window = UserDashboard(username="user")

        window.show()
        print("Application started successfully.")
        sys.exit(app.exec())

    except ImportError as e:
        error_msg = f"Missing required module: {e}"
        print(error_msg)
        QMessageBox.critical(None, "Import Error", error_msg)

    except Exception as e:
        error_msg = f"An unexpected error occurred:\n{e}"
        print(error_msg)
        QMessageBox.critical(None, "Application Error", error_msg)
    finally:
        app.quit()


if __name__ == "__main__":
    main()
