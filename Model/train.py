import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
import numpy as np
import random
from torch.utils.data import DataLoader, random_split
from model import AnomalyDetector
from utils.data_loader import NetworkDataset

# Set seeds for reproducibility
seed = 42
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyperparameters
csv_file = 'C:/Users/prath/OneDrive/Desktop/PROJECT/NETWORK ANAMOLY DETECTION/Data/processed/NetworkData.csv'
input_dim = 10  # Set according to your data
batch_size = 64
epochs = 50
lr = 1e-3
val_split = 0.2
patience = 5  # Early stopping patience

dataset = NetworkDataset(csv_file)
val_size = int(len(dataset) * val_split)
train_size = len(dataset) - val_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

model = AnomalyDetector(input_dim).to(device)
criterion = torch.nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

best_val_loss = float('inf')
epochs_no_improve = 0
os.makedirs('saved_models', exist_ok=True)

try:
    for epoch in range(epochs):
        model.train()
        train_losses = []
        for features, _ in train_loader:
            features = features.to(device)
            output = model(features)
            loss = criterion(output, features)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_losses.append(loss.item())
        avg_train_loss = np.mean(train_losses)

        # Validation
        model.eval()
        val_losses = []
        with torch.no_grad():
            for features, _ in val_loader:
                features = features.to(device)
                output = model(features)
                loss = criterion(output, features)
                val_losses.append(loss.item())
        avg_val_loss = np.mean(val_losses)

        print(f"Epoch {epoch+1}, Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}")

        # Early stopping and checkpointing
        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), 'saved_models/anomaly_detector.pth')
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                print("Early stopping triggered.")
                break
except KeyboardInterrupt:
    print("Training interrupted. Saving current model...")
    torch.save(model.state_dict(), 'saved_models/anomaly_detector_interrupt.pth')
