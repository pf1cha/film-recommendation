import pandas as pd
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer

pd.set_option('display.max_columns', None)
# Load dataset
data = pd.read_csv("../data/real_dataset.csv")

# Normalize numerical features
scaler = StandardScaler()
numerical_features = ["vote_average", "vote_count", "revenue", "runtime", "budget"]
data[numerical_features] = scaler.fit_transform(data[numerical_features])

# Process genres
data['genres'] = data['genres'].apply(lambda x: x.split(', '))
mlb = MultiLabelBinarizer()
genres_encoded = mlb.fit_transform(data['genres'])
genres_df = pd.DataFrame(genres_encoded, columns=mlb.classes_)

# languages_encoded = mlb.fit_transform(data['original_language'])
# language_df = pd.DataFrame(languages_encoded, columns=mlb.classes_)

# Combine all features
features = pd.concat([data[numerical_features], genres_df], axis=1)
