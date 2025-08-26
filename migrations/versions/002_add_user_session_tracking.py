
"""Add user session tracking

Adds fields for tracking user sessions and login attempts.
"""

from sqlalchemy import text

description = "Add user session tracking fields"


def upgrade(db):
    """Add session tracking fields"""
    
    # Add session tracking columns to users table
    try:
        db.execute(text("ALTER TABLE users ADD COLUMN last_ip VARCHAR(45)"))
    except Exception:
        pass  # Column might already exist
    
    try:
        db.execute(text("ALTER TABLE users ADD COLUMN login_attempts INTEGER DEFAULT 0"))
    except Exception:
        pass
    
    try:
        db.execute(text("ALTER TABLE users ADD COLUMN locked_until DATETIME"))
    except Exception:
        pass
    
    # Create user sessions table for active session tracking
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token VARCHAR(255) UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME NOT NULL,
            ip_address VARCHAR(45),
            user_agent TEXT,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """))
    
    # Create indexes
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token)"))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id)"))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at)"))


def downgrade(db):
    """Remove session tracking"""
    db.execute(text("DROP TABLE IF EXISTS user_sessions"))
    
    # Note: SQLite doesn't support DROP COLUMN, so we can't easily remove the added columns
    # In a production environment, you'd need to recreate the table
