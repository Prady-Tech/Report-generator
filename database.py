
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import os

# Create Base here
Base = declarative_base()

# SQLite database connection with better configuration
DATABASE_URL = "sqlite:///fortress_report.db"

# SQLAlchemy engine with optimized settings
engine = create_engine(
    DATABASE_URL, 
    connect_args={
        "check_same_thread": False,
        "timeout": 20,
        "isolation_level": None
    },
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def init_db():
    """Initialize database tables using migrations"""
    try:
        from migrations.migration_manager import MigrationManager
        manager = MigrationManager()
        manager.migrate()
        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")
        # Fallback to direct table creation for development
        print("Falling back to direct table creation...")
        Base.metadata.create_all(bind=engine)
        seed_default_users()


def seed_default_users():
    """Insert default users if they don't exist - fallback method"""
    from models import User
    
    with get_db_session() as db:
        try:
            default_users = [
                {"username": "admin", "password": "admin123", "role": "admin"},
                {"username": "user1", "password": "user123", "role": "user"},
            ]

            for u in default_users:
                existing = db.query(User).filter_by(username=u["username"]).first()
                if not existing:
                    new_user = User(username=u["username"], role=u["role"])
                    new_user.set_password(u["password"])
                    db.add(new_user)
                    
        except SQLAlchemyError as e:
            print(f"Database seeding error: {e}")
            raise


def verify_user(username, password):
    """Verify user credentials"""
    # Import here to avoid circular imports
    from models import User
    
    with get_db_session() as db:
        try:
            user = db.query(User).filter_by(username=username, is_active="true").first()
            if user and user.check_password(password):
                user.update_last_login()
                return True, user.role
            return False, None
        except SQLAlchemyError as e:
            print(f"User verification error: {e}")
            return False, None
