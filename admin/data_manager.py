# admin/data_manager.py

from database import SessionLocal
from models import User
from sqlalchemy.exc import SQLAlchemyError


class DataManager:
    """Handles database operations for Admin Dashboard"""

    def __init__(self):
        self.session = SessionLocal()

    def get_all_users(self):
        """Fetch all users (raw User objects)"""
        try:
            return self.session.query(User).all()
        except SQLAlchemyError as e:
            print(f"Error fetching users: {e}")
            return []

    def load_users_from_db(self):
        """Fetch all users as dictionaries (for UI)"""
        users_list = []
        try:
            users = self.get_all_users()
            for u in users:
                users_list.append({
                    "name": u.username,
                    "email": getattr(u, "email", "N/A"),  # fallback if no email field
                    "role": u.role
                })
        except Exception as e:
            print(f"Error loading users for UI: {e}")
        return users_list

    def add_user(self, username, password, role, email=None):
        """Add a new user"""
        try:
            new_user = User(username=username, role=role, email=email)
            new_user.set_password(password)
            self.session.add(new_user)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error adding user: {e}")
            return False

    def delete_user(self, username):
        """Delete a user by username"""
        try:
            user = self.session.query(User).filter_by(username=username).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error deleting user: {e}")
            return False

    def close(self):
        """Close the database session"""
        self.session.close()
