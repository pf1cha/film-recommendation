# File for creation a local database

import psycopg2
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Float
)

username = "postgres"
password = 12345
# Connection configuration (replace with your actual database credentials)
DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@localhost:5432/film_db"

# Create an engine and metadata object
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define Users table
users_table = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(50), nullable=False, unique=True),
    Column("hash_password", String(128), nullable=False)
)

# Define Content table
content_table = Table(
    "content", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("release_date", Date, nullable=False),
    Column("genre", String(50), nullable=False)
)

# Define UserInterests table
user_interests_table = Table(
    "user_interests", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("content_id", Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False),
    Column("score", Float, nullable=False)  # User's rating/score for the content
)

# Create tables in the database
if __name__ == "__main__":
    metadata.create_all(engine)
    print("Tables created successfully!")