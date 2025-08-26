# db.py - Legacy authentication module (replaced by database.py)
from database import verify_user as db_verify_user, init_db as db_init

def verify_user(username, password):
    """Legacy wrapper for user verification"""
    return db_verify_user(username, password)

def init_db():
    """Legacy wrapper for database initialization"""
    return db_init()