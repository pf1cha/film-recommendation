from data_preparation import features
import torch.nn as nn
import torch
import torch.optim as optim
import numpy as np


class MovieAutoencoder(nn.Module):
    def __init__(self, input_dim, embedding_dim=32):
        super(MovieAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, embedding_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(embedding_dim, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        embedding = self.encoder(x)
        reconstruction = self.decoder(embedding)
        return embedding, reconstruction


features_tensor = torch.tensor(features.values, dtype=torch.float)
# Initialize the model
model = MovieAutoencoder(input_dim=features_tensor.shape[1])

# Define loss and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Prepare data for training
dataset = torch.utils.data.TensorDataset(features_tensor)
data_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

# Training the autoencoder
epochs = 50
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in data_loader:
        inputs = batch[0]
        # Forward pass
        optimizer.zero_grad()
        embeddings, reconstructed = model(inputs)
        # Compute loss
        loss = criterion(reconstructed, inputs)
        total_loss += loss.item()
        # Backward pass and optimization
        loss.backward()
        optimizer.step()

# # Switch the model to evaluation mode
# model.eval()
# # Example: Get recommendations for the first movie
# torch.save(model.state_dict(), "movie2movie_recommender.pth")

# Compute embeddings
with torch.no_grad():
    embeddings, _ = model(features_tensor)

# Save embeddings to a file
np.save("movie2movie_embeddings.npy", embeddings.numpy())
