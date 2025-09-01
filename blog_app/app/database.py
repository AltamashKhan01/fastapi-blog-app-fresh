# Import necessary modules from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

# Create a new SQLAlchemy engine instance
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a new sessionmaker instance
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create a declarative base instance
Base = declarative_base()


# Dependency to get a database session
def get_db():
    """
    This function is a dependency that provides a database session.
    It ensures that the database session is always closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()