# main.py
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from database import init_db, SessionLocal
from models import User
from auth import run_login  # our PySide6 login

def seed_users():
    """Seed default users into the database without duplication."""
    session = SessionLocal()
    try:
        # Admin
        if not session.query(User).filter_by(username="admin").first():
            session.add(User(username="admin", password="admin123", role="admin"))

        # Normal user
        if not session.query(User).filter_by(username="user").first():
            session.add(User(username="user", password="user123", role="user"))

        session.commit()
    except Exception as e:
        print(f"Error while seeding users: {e}")
        session.rollback()
    finally:
        session.close()


def main():
    """Entry point for the application."""
    app = QApplication(sys.argv)

    try:
        # Initialize database and seed default users
        init_db()
        seed_users()

        # Show login window
        role = run_login()  # run_login returns the role or None
        if not role:
            QMessageBox.warning(None, "Login Failed", "Invalid username or password or login canceled.")
            return

        # Launch appropriate dashboard
        if role == "admin":
            from admin_dashboard import AdminDashboard
            window = AdminDashboard()
        else:
            from user_dashboard import UserDashboard
            window = UserDashboard()

        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Application Error", f"An unexpected error occurred:\n{e}")
        app.quit()


if __name__ == "__main__":
    main()
