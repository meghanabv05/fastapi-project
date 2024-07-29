import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from app.config import settings
import logging

# Configure logging to suppress SQLAlchemy engine logs
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

# Create SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)  # Set echo=False to suppress SQL logs

# Create SQLAlchemy session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Establish a connection to the database using psycopg2
try:
    conn = psycopg2.connect(
        host=settings.database_host,
        database=settings.database_name,
        user=settings.database_username,
        password=settings.database_password,
        cursor_factory=RealDictCursor
    )
    with conn.cursor() as cursor:
        print("Database connection was successful")
except Exception as error:
    print("Connecting to database failed")
    print("Error was:", error)