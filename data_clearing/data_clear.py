import pandas as pd


pd.set_option('display.max_columns', None)

def parse_recommended_films(recommended_films):
    recommended_films = recommended_films.replace('-', ', ')
    return recommended_films

def combine_companies(comp1, comp2):
    """ Handle production_companies (combine and remove duplicates)
    :param comp1: string which contains the company
    :param comp2: string which contains the company
    :return: the combine company
    """
    if pd.isna(comp1) or "unknown" == comp1: comp1 = ""
    if pd.isna(comp2) or "unknown" == comp2 : comp2 = ""
    combined = list(dict.fromkeys(comp1.split(', ') + comp2.split(', ')))
    return ', '.join([comp for comp in combined if comp])


def combine_genres(genres1, genres2):
    """ combine two strings which contains the data in csv format
    ::return:: one string with unique data
    """
    genres1_list = [g.strip() for g in genres1.split(',')]
    genres2_list = [g.strip() for g in genres2.split(',')]
    combined_genres = list(dict.fromkeys(genres1_list + genres2_list))
    return ', '.join(combined_genres)


def merge_the_same_columns(merged_df):
    merged_df['popularity'] = merged_df[['popularity_df1', 'popularity_df2']].mean(axis=1)
    merged_df['vote_average'] = (((merged_df['vote_count_df1'] * merged_df['vote_average_df1']) +
                                (merged_df['vote_count_df2'] * merged_df['vote_average_df2']))
                                / (merged_df['vote_count_df1'] + merged_df['vote_count_df2']))
    merged_df['vote_count'] = merged_df['vote_count_df1'] + merged_df['vote_count_df2']
    merged_df['genres'] = merged_df.apply(lambda row: combine_genres(
        row['genres_df1'], row['genres_df2']), axis=1)

    merged_df['release_date'] = merged_df['release_date_df1'].combine_first(merged_df['release_date_df2'])

    merged_df['revenue'] = merged_df['revenue_df1'].fillna(0) + merged_df['revenue_df2'].fillna(0)

    merged_df['runtime'] = merged_df[['runtime_df1', 'runtime_df2']].mean(axis=1)

    merged_df['budget'] = merged_df[['budget_df1', 'budget_df2']].mean(axis=1)

    merged_df['original_language'] = merged_df['original_language_df1'].combine_first(
        merged_df['original_language_df2'])

    merged_df['production_companies'] = merged_df.apply(lambda row: combine_companies(
        row['production_companies_df1'], row['production_companies_df2']), axis=1)

    merged_df = merged_df.drop(columns=[
        'popularity_df1', 'popularity_df2', 'vote_average_df1', 'vote_average_df2',
        'vote_count_df1', 'vote_count_df2', 'release_date_df1', 'release_date_df2',
        'revenue_df1', 'revenue_df2', 'runtime_df1', 'runtime_df2', 'budget_df1',
        'budget_df2', 'original_language_df1', 'original_language_df2',
        'production_companies_df1', 'production_companies_df2', 'genres_df1', 'genres_df2',
    ])
    return merged_df

if __name__ == '__main__':
    # https://www.kaggle.com/datasets/akshaypawar7/millions-of-movies
    films_2 = pd.read_csv('../data/movies.csv')
    films_2 = films_2[films_2["vote_count"] >= 10]
    films_2 = films_2.drop(["overview", "status", "tagline",
                            "credits", "keywords", "poster_path",
                            "backdrop_path"], axis=1)
    # https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies/data
    films_3 = pd.read_csv('../data/tmdb_movies.csv')
    films_3 = films_3[films_3["vote_count"] >= 10]
    films_3 = films_3.drop(["id", "status", "adult", "backdrop_path",
                            "homepage", "imdb_id", "original_title",
                            "overview", "poster_path", "tagline",
                            "spoken_languages", "keywords", "production_countries"], axis=1)
    films_2['release_date'] = pd.to_datetime(films_2['release_date'])
    films_3['release_date'] = pd.to_datetime(films_3['release_date'])
    films_2['genres'] = films_2['genres'].fillna('unknown')
    films_2['production_companies'] = films_2['production_companies'].fillna('unknown')
    films_3['genres'] = films_3['genres'].fillna('unknown')
    films_3['production_companies'] = films_3['production_companies'].fillna('unknown')

    merged_films = pd.merge(films_2, films_3, on='title', suffixes=('_df1', '_df2'))
    merged_films = merge_the_same_columns(merged_films)

    merged_films = merged_films.drop_duplicates(subset=['title'], keep='first')
    merged_films = merged_films.drop(['popularity', 'production_companies', 'recommendations'], axis=1)
    print(str(merged_films.head()))
    # Turning categorical variables into quantitative variables
    # merged_films = pd.get_dummies(merged_films)
    # print(merged_films.shape)

    # Make a histogram

    # id,title,recommendations,popularity,vote_average,vote_count,genres,release_date,revenue,runtime,budget,original_language,production_companies