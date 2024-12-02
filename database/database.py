from sqlalchemy import create_engine, Column, Integer, String, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import configparser
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Float
)
from db_password import DATABASE_URL

Base = declarative_base()

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

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    db_config = {
        "host": config["DATABASE"]["HOST"],
        "port": config["DATABASE"]["PORT"],
        "user": config["DATABASE"]["USER"],
        "password": config["DATABASE"]["PASSWORD"],
        "dbname": config["DATABASE"]["DB_NAME"]
    }
    return db_config


def get_session():
    config_db = load_config()
    engine = get_connection(config_db)
    session = sessionmaker(bind=engine)
    return session

def get_connection(db_config):
    return create_engine(DATABASE_URL, echo=True, future=True)

def add_user(username, hashed_password):
    print("step 1")
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    print("step 2")
    stmt = insert(users_table).values(username=username, hash_password=hashed_password)
    print(stmt)
    try:
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
        return "User registered successfully."
    except IntegrityError:
        return "Username already exists."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def initialize_database():
    db_config = load_config()
    engine = get_connection(db_config)
    Base.metadata.create_all(engine)