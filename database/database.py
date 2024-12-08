from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import configparser
from sqlalchemy import (
    create_engine, select, desc, insert
)
from sqlalchemy.orm import Session
from database.db_password import DATABASE_URL
from database.database_info import users_table, content_table

Base = declarative_base()


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


def fetch_movies(offset=0, limit=10):
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine)  # Replace 'engine' with your SQLAlchemy engine
    try:
        query = select(content_table).order_by(desc(content_table.c.vote_average)).limit(limit).offset(offset)
        result = session.execute(query).fetchall()
        return result
    finally:
        session.close()
