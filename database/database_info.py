from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Float
)


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
    Column("genre", String(50), nullable=False),
    Column("revenue", Float),  # Newly added
    Column("runtime", Float),  # Newly added
    Column("vote_average", Float),  # Newly added
    Column("vote_count", Integer),  # Newly added
    Column("budget", Float),  # Newly added
    Column("original_language", String(10))  # Newly added
)

# Define UserInterests table
user_interests_table = Table(
    "user_interests", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("content_id", Integer, ForeignKey("content.id", ondelete="CASCADE"), nullable=False),
    Column("score", Float, nullable=False)  # User's rating/score for the content
)
