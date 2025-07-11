import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    # Fill missing values, encode categorical, etc.
    df = df.fillna(0)
    scaler = StandardScaler()
    df[df.columns[:-1]] = scaler.fit_transform(df[df.columns[:-1]])
    df.to_csv(output_csv, index=False)
