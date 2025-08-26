# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

#  Create Base here
Base = declarative_base()

# SQLite database connection
DATABASE_URL = "sqlite:///fortress_report.db"

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    import models  # Import here to avoid circular import
    Base.metadata.create_all(bind=engine)


def seed_users():
    """Insert default users if they don't exist"""
    from models import User  # Import here to avoid circular import
    db = SessionLocal()
    try:
        default_users = [
            {"username": "admin", "password": "admin123", "role": "admin"},
            {"username": "user1", "password": "user123", "role": "user"},
        ]

        for u in default_users:
            existing = db.query(User).filter_by(username=u["username"]).first()
            if not existing:
                new_user = User(username=u["username"], password=u["password"], role=u["role"])
                db.add(new_user)

        db.commit()
    except SQLAlchemyError as e:
        print(f"Database seeding error: {e}")
        db.rollback()
    finally:
        db.close()
