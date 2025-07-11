import pandas as pd
from torch.utils.data import Dataset

class NetworkDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = self.data.iloc[idx, :-1].values.astype('float32')
        label = self.data.iloc[idx, -1]
        if self.transform:
            features = self.transform(features)
        return features, label
