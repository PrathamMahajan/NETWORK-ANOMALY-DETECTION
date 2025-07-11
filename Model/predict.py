import torch
from Model.model import AnomalyDetector

def predict(input_features, model_path, threshold):
    input_dim = len(input_features)
    model = AnomalyDetector(input_dim)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    input_tensor = torch.tensor(input_features, dtype=torch.float32)
    with torch.no_grad():
        reconstructed = model(input_tensor)
        loss = torch.nn.functional.mse_loss(reconstructed, input_tensor)
        is_anomaly = loss.item() > threshold
    return is_anomaly, loss.item()
