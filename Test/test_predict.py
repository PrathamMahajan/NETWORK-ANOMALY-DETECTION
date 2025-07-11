import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
from Model.predict import predict

# Example test function for the predict function
def test_predict():
    # Example input (replace with a real sample from your data)
    input_features = [0.3232235816, 0.347974920, 60238.0, 443.0, 1.0, 4719.0, 0.0, 12.0, 0.0, 1.2789263725280762]
    model_path = os.path.join('..', 'Model', 'saved_models', 'Trained_Model.pth')
    threshold = 0.000005  # Set this based on your validation analysis

    is_anomaly, loss = predict(input_features, model_path, threshold)
    print(f"Is Anomaly: {is_anomaly}, Reconstruction Loss: {loss}")

if __name__ == "__main__":
    test_predict()
