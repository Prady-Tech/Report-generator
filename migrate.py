
#!/usr/bin/env python3
"""
Database Migration Script for Fortress Report

Usage:
    python migrate.py              # Run all pending migrations
    python migrate.py status       # Show migration status
    python migrate.py rollback <migration_id>  # Rollback specific migration
"""

import sys
from migrations.migration_manager import MigrationManager


def main():
    manager = MigrationManager()
    
    if len(sys.argv) == 1:
        # Run migrations
        manager.migrate()
    elif sys.argv[1] == "status":
        # Show status
        manager.status()
    elif sys.argv[1] == "rollback" and len(sys.argv) == 3:
        # Rollback specific migration
        migration_id = sys.argv[2]
        manager.rollback(migration_id)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
