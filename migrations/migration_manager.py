
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from database import engine, get_db_session
from sqlalchemy import text
import importlib.util


class MigrationManager:
    def __init__(self):
        self.migrations_dir = Path(__file__).parent / "versions"
        self.migrations_dir.mkdir(exist_ok=True)
        self.ensure_migration_table()
    
    def ensure_migration_table(self):
        """Create migration tracking table if it doesn't exist"""
        with get_db_session() as db:
            db.execute(text("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    migration_id VARCHAR(50) UNIQUE NOT NULL,
                    applied_at DATETIME NOT NULL,
                    description TEXT
                )
            """))
    
    def get_applied_migrations(self):
        """Get list of applied migrations"""
        with get_db_session() as db:
            result = db.execute(text("SELECT migration_id FROM schema_migrations ORDER BY applied_at"))
            return [row[0] for row in result.fetchall()]
    
    def get_pending_migrations(self):
        """Get list of pending migrations"""
        applied = set(self.get_applied_migrations())
        all_migrations = []
        
        for file in sorted(self.migrations_dir.glob("*.py")):
            if file.name != "__init__.py":
                migration_id = file.stem
                if migration_id not in applied:
                    all_migrations.append(migration_id)
        
        return all_migrations
    
    def run_migration(self, migration_id):
        """Run a specific migration"""
        migration_file = self.migrations_dir / f"{migration_id}.py"
        
        if not migration_file.exists():
            raise FileNotFoundError(f"Migration {migration_id} not found")
        
        # Load migration module
        spec = importlib.util.spec_from_file_location("migration", migration_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run upgrade
        with get_db_session() as db:
            try:
                module.upgrade(db)
                
                # Record migration as applied
                db.execute(text("""
                    INSERT INTO schema_migrations (migration_id, applied_at, description)
                    VALUES (:migration_id, :applied_at, :description)
                """), {
                    "migration_id": migration_id,
                    "applied_at": datetime.utcnow(),
                    "description": getattr(module, 'description', 'No description')
                })
                
                print(f"Applied migration: {migration_id}")
                
            except Exception as e:
                print(f"Failed to apply migration {migration_id}: {e}")
                raise
    
    def migrate(self):
        """Run all pending migrations"""
        pending = self.get_pending_migrations()
        
        if not pending:
            print("No pending migrations.")
            return
        
        print(f"Found {len(pending)} pending migrations:")
        for migration_id in pending:
            self.run_migration(migration_id)
        
        print("All migrations completed successfully!")
    
    def rollback(self, migration_id):
        """Rollback a specific migration"""
        migration_file = self.migrations_dir / f"{migration_id}.py"
        
        if not migration_file.exists():
            raise FileNotFoundError(f"Migration {migration_id} not found")
        
        # Load migration module
        spec = importlib.util.spec_from_file_location("migration", migration_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run downgrade
        with get_db_session() as db:
            try:
                if hasattr(module, 'downgrade'):
                    module.downgrade(db)
                    
                    # Remove migration record
                    db.execute(text("""
                        DELETE FROM schema_migrations WHERE migration_id = :migration_id
                    """), {"migration_id": migration_id})
                    
                    print(f"Rolled back migration: {migration_id}")
                else:
                    print(f"Migration {migration_id} does not support rollback")
                    
            except Exception as e:
                print(f"Failed to rollback migration {migration_id}: {e}")
                raise
    
    def status(self):
        """Show migration status"""
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()
        
        print(f"Applied migrations ({len(applied)}):")
        for migration in applied:
            print(f"  ✓ {migration}")
        
        print(f"\nPending migrations ({len(pending)}):")
        for migration in pending:
            print(f"  ⏳ {migration}")
