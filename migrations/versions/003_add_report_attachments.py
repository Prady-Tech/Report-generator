
"""Add report attachments

Adds support for file attachments to reports.
"""

from sqlalchemy import text

description = "Add report attachments support"


def upgrade(db):
    """Add report attachments table"""
    
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS report_attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            filename VARCHAR(255) NOT NULL,
            original_filename VARCHAR(255) NOT NULL,
            file_size INTEGER NOT NULL,
            content_type VARCHAR(100),
            file_path TEXT NOT NULL,
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (report_id) REFERENCES reports (id) ON DELETE CASCADE
        )
    """))
    
    # Add indexes
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_attachments_report_id ON report_attachments(report_id)"))
    db.execute(text("CREATE INDEX IF NOT EXISTS idx_attachments_filename ON report_attachments(filename)"))
    
    # Add priority field to reports
    try:
        db.execute(text("ALTER TABLE reports ADD COLUMN priority VARCHAR(20) DEFAULT 'Normal'"))
    except Exception:
        pass
    
    try:
        db.execute(text("ALTER TABLE reports ADD COLUMN category VARCHAR(50)"))
    except Exception:
        pass


def downgrade(db):
    """Remove report attachments"""
    db.execute(text("DROP TABLE IF EXISTS report_attachments"))
