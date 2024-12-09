import torch
import pandas as pd
from torch.nn.functional import cosine_similarity
import numpy as np

pd.set_option('display.max_columns', None)
def recommend_movies_with_model(db_movie_id, top_k=5):
    embeddings = torch.tensor(np.load("model/movie2movie_embeddings.npy"), dtype=torch.float)
    data = pd.read_csv("data/real_dataset.csv")
    if db_movie_id not in data['id'].values:
        return []
    movie_id = data[data['id'] == db_movie_id].index[0]
    # Target movie embedding
    target_embedding = embeddings[movie_id]
    # Compute cosine similarity
    similarities = cosine_similarity(target_embedding.unsqueeze(0), embeddings)
    # Get top_k most similar movies (excluding the target movie)
    similar_movies = similarities.squeeze().argsort(descending=True)[1:top_k + 1]
    return data.iloc[similar_movies.tolist()]['id'].values
