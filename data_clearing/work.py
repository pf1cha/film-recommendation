import pandas as pd

pd.set_option('display.max_columns', None)

merged_films = pd.read_csv('../data/films_merged.csv')
merged_films = merged_films.drop_duplicates(subset=['title'], keep='first')
merged_films = merged_films.drop(['popularity', 'production_companies', 'recommendations'], axis=1)

# Replace hyphens with commas in the genres column
merged_films['genres'] = merged_films['genres'].str.replace('-', ', ')

# Remove duplicate genres for each film
merged_films['genres'] = merged_films['genres'].apply(lambda x: ', '.join(set(x.split(', '))))

# Split the genres into individual entries
all_genres = merged_films['genres'].str.split(', ')

# Flatten the list of genres
flattened_genres = [genre for sublist in all_genres for genre in sublist]

# Count the occurrences of each genre
genre_counts = pd.Series(flattened_genres).value_counts()

print(merged_films.info())
