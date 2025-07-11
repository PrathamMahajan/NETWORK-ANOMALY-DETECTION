# Network Anomaly Detection (Deep Learning)

## Project Structure

- `Data/` - Raw and processed data
- `Model/` - Model code, training, evaluation, and saved models
- `Notebook/` - Jupyter notebooks for EDA and prototyping
- `utils/` - Utility scripts (data loading, preprocessing, etc.)
- `requirements.txt` - Python dependencies

## Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Preprocess data:
   ```python
   from utils.preprocessing import preprocess_data
   preprocess_data('Data/NetworkData.csv', 'Data/processed/processed_data.csv')
   ```
3. Train model:
   ```sh
   python Model/train.py
   ```
4. Predict (real-time):
   ```python
   from Model.predict import predict
   is_anomaly, score = predict(input_features, 'Model/saved_models/anomaly_detector.pth', threshold=0.1)
   ```

## Notes

- Adjust `input_dim` in `Model/train.py` and model architecture as per your data.
- Add more utility scripts or modules as needed for metrics, logging, etc.
