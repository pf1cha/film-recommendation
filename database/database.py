from sqlalchemy import create_engine, Column, Integer, String, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import configparser
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Float
)
from database.db_password import DATABASE_URL
from database.database_info import users_table

Base = declarative_base()

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
    engine = create_engine(DATABASE_URL, echo=True, future=True)
    stmt = insert(users_table).values(username=username, hash_password=hashed_password)
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