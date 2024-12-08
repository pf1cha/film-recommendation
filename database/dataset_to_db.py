import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, insert
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db_password import DATABASE_URL
from database_info import content_table
from sqlalchemy.exc import IntegrityError

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect the existing table
movies_table = Table('content', metadata, autoload_with=engine)

# Read the dataset
df = pd.read_csv('../data/real_dataset.csv')

# Parse the release_date to proper format
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Convert NaN values to None (SQL-friendly)
df = df.where(pd.notnull(df), None)

# Establish Session
Session = sessionmaker(bind=engine)
session = Session()


# Function to insert a record while handling duplicates
def insert_record(session, row):
    if len(row['title']) < 100:
        stmt = insert(content_table).values(
            id=row['id'],
            name=row['title'],
            vote_average=row['vote_average'],
            vote_count=row['vote_count'],
            genre=row['genres'].split(', ')[0],
            release_date=row['release_date'],
            revenue=row['revenue'],
            runtime=row['runtime'],
            budget=row['budget'],
            original_language=row['original_language']
        )
        try:
            session.execute(stmt)
            session.commit()
        except IntegrityError:
            session.rollback()
            print(f"Duplicate ID error for record with ID: {row['id']}")


# Insert records by calling the insert_record function
for _, row in df.iterrows():
    insert_record(session, row)

# Close the session
session.close()
