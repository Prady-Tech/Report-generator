
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class DataPersistenceManager:
    def __init__(self, data_dir: str = "user_data"):
        """Initialize data persistence manager"""
        self.data_dir = data_dir
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_user_data_file(self, username: str) -> str:
        """Get the file path for a user's data"""
        safe_username = username.replace(" ", "_").lower()
        return os.path.join(self.data_dir, f"{safe_username}_data.json")
    
    def save_user_session(self, username: str, session_data: Dict[str, Any]) -> bool:
        """Save user session data to JSON file"""
        try:
            file_path = self.get_user_data_file(username)
            
            # Add metadata
            session_data.update({
                "last_saved": datetime.now().isoformat(),
                "username": username,
                "version": "1.0"
            })
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print(f"Session data saved for user: {username}")
            return True
            
        except Exception as e:
            print(f"Error saving session data for {username}: {e}")
            return False
    
    def load_user_session(self, username: str) -> Optional[Dict[str, Any]]:
        """Load user session data from JSON file"""
        try:
            file_path = self.get_user_data_file(username)
            
            if not os.path.exists(file_path):
                print(f"No session data found for user: {username}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            print(f"Session data loaded for user: {username}")
            return session_data
            
        except Exception as e:
            print(f"Error loading session data for {username}: {e}")
            return None
    
    def clear_user_session(self, username: str) -> bool:
        """Clear user session data"""
        try:
            file_path = self.get_user_data_file(username)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Session data cleared for user: {username}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error clearing session data for {username}: {e}")
            return False
    
    def get_default_session_data(self) -> Dict[str, Any]:
        """Get default session data structure"""
        return {
            "ui_state": {
                "last_page": "dashboard",
                "window_geometry": {
                    "x": 100,
                    "y": 100,
                    "width": 1200,
                    "height": 700
                },
                "search_filters": {},
                "table_columns_width": {}
            },
            "user_preferences": {
                "theme": "dark",
                "notifications_enabled": True,
                "auto_save_interval": 30
            },
            "work_progress": {
                "draft_reports": [],
                "unsaved_changes": {},
                "bookmarks": []
            }
        }
