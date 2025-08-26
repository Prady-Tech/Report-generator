
import bcrypt
from database import get_db_session
from models import User

def fix_passwords():
    """Fix the password hashes for default users"""
    
    # Generate correct password hashes
    admin_password = "admin123"
    user_password = "user123"
    
    admin_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_hash = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    print(f"Admin hash: {admin_hash}")
    print(f"User hash: {user_hash}")
    
    # Update database
    with get_db_session() as db:
        # Update admin password
        admin_user = db.query(User).filter_by(username="admin").first()
        if admin_user:
            admin_user.password_hash = admin_hash
            print("Updated admin password hash")
        
        # Update user1 password
        regular_user = db.query(User).filter_by(username="user1").first()
        if regular_user:
            regular_user.password_hash = user_hash
            print("Updated user1 password hash")
        
        print("Password hashes updated successfully!")

if __name__ == "__main__":
    fix_passwords()
