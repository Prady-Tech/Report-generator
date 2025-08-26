
#!/usr/bin/env python3
"""
Create new migration script

Usage:
    python create_migration.py "Description of changes"
"""

import sys
from datetime import datetime
from pathlib import Path


def create_migration(description):
    """Create a new migration file"""
    migrations_dir = Path("migrations/versions")
    migrations_dir.mkdir(parents=True, exist_ok=True)
    
    # Get next migration number
    existing_migrations = list(migrations_dir.glob("*.py"))
    existing_migrations = [f for f in existing_migrations if f.name != "__init__.py"]
    
    if existing_migrations:
        # Extract numbers from existing migrations
        numbers = []
        for f in existing_migrations:
            name = f.stem
            if name.split("_")[0].isdigit():
                numbers.append(int(name.split("_")[0]))
        next_num = max(numbers) + 1 if numbers else 1
    else:
        next_num = 1
    
    # Create migration filename
    safe_description = description.lower().replace(" ", "_").replace("-", "_")
    safe_description = "".join(c for c in safe_description if c.isalnum() or c == "_")
    
    migration_id = f"{next_num:03d}_{safe_description}"
    migration_file = migrations_dir / f"{migration_id}.py"
    
    # Migration template
    template = f'''"""
{description}

Migration: {migration_id}
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

from sqlalchemy import text

description = "{description}"


def upgrade(db):
    """Apply migration changes"""
    # Add your migration logic here
    # Example:
    # db.execute(text("ALTER TABLE users ADD COLUMN new_field VARCHAR(100)"))
    pass


def downgrade(db):
    """Rollback migration changes"""
    # Add your rollback logic here
    # Example:
    # db.execute(text("ALTER TABLE users DROP COLUMN new_field"))
    pass
'''
    
    # Write migration file
    migration_file.write_text(template)
    print(f"Created migration: {migration_file}")
    print(f"Migration ID: {migration_id}")
    
    return migration_id


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    description = sys.argv[1]
    create_migration(description)


if __name__ == "__main__":
    main()
