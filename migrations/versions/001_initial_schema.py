
"""Initial schema migration

Creates the basic user and report tables with proper constraints and indexes.
"""

from sqlalchemy import text

description = "Initial schema - create users and reports tables"


def upgrade(db):
    """Create initial schema"""
    
    # Create users table
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'user',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME,
            is_active VARCHAR(10) DEFAULT 'true'
        )
    """))
    
    # Create indexes for users table
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)"))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)"))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active)"))
    
    # Create reports table
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100) NOT NULL,
            content TEXT NOT NULL,
            status VARCHAR(20) DEFAULT 'Pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """))
    
    # Create indexes for reports table
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_reports_user_id ON reports(user_id)"))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status)"))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_reports_created_at ON reports(created_at)"))
    
    # Insert default admin user (password: admin123)
    db.execute(text("""
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES ('admin', '$2b$12$8Xk7zQXKjx5E.bF5sYvQvOzY6TtxMQJqhN8/LeGCB6OvNX.V6MJHS', 'admin')
    """))
    
    # Insert default regular user (password: user123)
    db.execute(text("""
        INSERT OR IGNORE INTO users (username, password_hash, role) 
        VALUES ('user1', '$2b$12$9Yl8aRYLky6F.cG6tZwRwPaZ7UuxNRKriO9/MfHDB7PwOY.W7NKIS', 'user')
    """))


def downgrade(db):
    """Drop initial schema"""
    db.execute(text("DROP TABLE IF EXISTS reports"))
    db.execute(text("DROP TABLE IF EXISTS users"))
