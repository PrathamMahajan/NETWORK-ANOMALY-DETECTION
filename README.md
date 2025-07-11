# Network Anomaly Detection (Deep Learning)

A deep learning-based system for real-time network anomaly detection using flow-level features.

## Project Structure

- `Data/`
  - Raw and processed network data files.
- `Model/`
  - Model architecture, training scripts, prediction logic, and saved models.
- `Notebook/`
  - Jupyter notebooks for exploratory data analysis (EDA), prototyping, and visualization.
    - `main.ipynb` – EDA and feature analysis.
    - `train_model.ipynb` – Model training and validation.
- `NetworkTrafficCapture/`
  - Real-time network traffic capture and flow extraction (`Capture.py`).
- `utils/`
  - Utility scripts for data loading (`data_loader.py`), preprocessing (`preprocessing.py`), etc.
- `Test/`
  - Unit and integration tests (`test_predict.py`).
- `main.py`
  - Entry point for real-time anomaly detection using the trained model.
- `requirements.txt`
  - Python dependencies.

## Setup

1. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

2. **Preprocess data:**

   ```python
   from utils.preprocessing import preprocess_data
   preprocess_data('Data/NetworkData.csv', 'Data/processed/processed_data.csv')
   ```

3. **Train the model:**

   - Use the notebook (`Notebook/train_model.ipynb`) for interactive training and validation.
   - Or run the training script:
     ```sh
     python Model/train.py
     ```

4. **Real-time prediction:**
   - Run the main script to start live anomaly detection:
     ```sh
     python main.py
     ```
   - Or use the prediction module directly:
     ```python
     from Model.predict import predict
     is_anomaly, score = predict(input_features, 'Model/saved_models/anomaly_detector.pth', threshold=0.1)
     ```

## Usage

- **Feature Extraction:**  
  Network flows are captured and converted to feature vectors in `main.py` using `NetworkTrafficCapture/Capture.py`.
- **Model Inference:**  
  The trained model predicts anomalies based on flow features.
- **Thresholds:**  
  Adjust the anomaly threshold in `main.py` or prediction calls as needed.

## Notes

- Ensure the feature order and dimensions in `main.py` and model scripts match your data.
- Update `input_dim` in `Model/train.py` and model architecture if your feature set changes.
- Extend utility scripts for additional metrics, logging, or custom preprocessing.
- Use the provided notebooks for data exploration and model evaluation.

## Testing

- Run unit tests in the `Test/` folder to validate prediction and utility functions:
  ```sh
  python -m unittest discover Test
  ```

## License

MIT License (add or update as
