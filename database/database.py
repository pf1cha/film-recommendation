import configparser
from sqlalchemy import create_engine, select, desc, insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from database.db_password import DATABASE_URL
from database.database_info import users_table, content_table, user_interests_table
from utils.utils import hash_password

Base = declarative_base()

# Create an engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def add_user(username, hashed_password):
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

def authenticate_user(username: str, password: str):
    session = SessionLocal()
    try:
        user = session.query(users_table).filter_by(username=username).one_or_none()
        if user is None:
            return "User not found.", None
        hashed_password = hash_password(password)
        if hashed_password == user.hash_password:
            return "Authentication successful.", user.id
        else:
            return "Invalid password.", None
    except Exception as e:
        session.rollback()
        return f"An error occurred: {str(e)}", None
    finally:
        session.close()

def fetch_movies(offset=0, limit=10):
    session = SessionLocal()
    try:
        query = select(content_table).order_by(desc(content_table.c.vote_average)).limit(limit).offset(offset)
        result = session.execute(query).fetchall()
        return result
    finally:
        session.close()

def fetch_movies_by_title(title: str, genre=None, min_rating=None, max_rating=None, year=None, limit=None, offset=0):
    session = SessionLocal()
    try:
        query = select(content_table).where(content_table.c.name.ilike(f"%{title}%"))
        if genre:
            query = query.where(content_table.c.genre == genre)
        if min_rating:
            query = query.where(content_table.c.rating >= min_rating)
        if max_rating:
            query = query.where(content_table.c.rating <= max_rating)
        if year:
            query = query.where(content_table.c.release_year == year)
        if limit is not None:
            query = query.limit(limit).offset(offset)
        results = session.execute(query).fetchall()
        return results
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return []
    finally:
        session.close()

def add_or_update_user_rating(user_id: int, movie_id: int, rating: float):
    session = SessionLocal()
    try:
        existing_rating = session.execute(
            select(user_interests_table)
            .where(user_interests_table.c.user_id == user_id)
            .where(user_interests_table.c.content_id == movie_id)
        ).scalar_one_or_none()
        if existing_rating:
            stmt = update(user_interests_table).where(
                user_interests_table.c.user_id == user_id,
                user_interests_table.c.content_id == movie_id
            ).values(score=rating)
            session.execute(stmt)
            session.commit()
            return "Rating updated successfully."
        else:
            stmt = insert(user_interests_table).values(user_id=user_id, content_id=movie_id, score=rating)
            session.execute(stmt)
            session.commit()
            return "Rating added successfully."
    except IntegrityError as e:
        session.rollback()
        return f"Database integrity error: {str(e)}"
    except Exception as e:
        session.rollback()
        return f"An error occurred: {str(e)}"
    finally:
        session.close()

def fetch_films_by_ids(film_ids):
    if not film_ids:
        return []
    session = SessionLocal()
    try:
        query = select(content_table).where(content_table.c.id.in_(film_ids))
        result = session.execute(query).fetchall()
        return result
    except Exception as e:
        print(f"Error fetching films: {e}")
        return []
    finally:
        session.close()

def is_id_in_table(id):
    session = SessionLocal()
    try:
        query = select(content_table).where(content_table.c.id == id)
        result = session.execute(query).fetchone()
        return result is not None
    except Exception as e:
        session.close()
        raise e
    finally:
        session.close()

def get_film_id_by_name(film_name):
    session = SessionLocal()
    try:
        query = select(content_table).where(content_table.c.name.ilike(f"{film_name}"))
        result = session.execute(query).fetchone()
        if result:
            return result.id
        else:
            return None
    except Exception as e:
        session.close()
        raise e
    finally:
        session.close()

def fetch_user_reviews(user_id):
    session = SessionLocal()
    try:
        query = select(user_interests_table).where(user_interests_table.c.user_id == user_id)
        result = session.execute(query).fetchall()
        return result
    except Exception as e:
        session.close()
        raise e
    finally:
        session.close()

def get_film_title_by_id(film_id):
    """
    Fetch the film title by its ID from the database.

    Args:
        film_id (int): The ID of the film to fetch.

    Returns:
        str: The title of the film, or None if not found.
    """
    session = SessionLocal()
    try:
        result = session.query(content_table.c.name).filter(content_table.c.id == film_id).first()
        if result:
            title = result[0]  # Extract the name from the tuple
            return title
        print(f"Title not found for film ID: {film_id}")
        return None
    except Exception as e:
        print(f"Error fetching title for film ID {film_id}: {e}")
        return None
    finally:
        session.close()