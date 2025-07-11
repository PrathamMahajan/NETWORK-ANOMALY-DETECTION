from NetworkTrafficCapture.Capture import capture_flows
from Model.predict import predict
import struct
import socket

MODEL_PATH = 'Model/saved_models/Trained_Model.pth'
THRESHOLD = 0.00005  # Adjust as needed

def ip_to_int(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except Exception:
        return 0.0

def on_flow_update(flow_key, flow):
    # Convert flow dict to feature vector in required order
    input_features = [
        ip_to_int(flow.get('SourceIP', '0.0.0.0')),
        ip_to_int(flow.get('DestinationIP', '0.0.0.0')),
        float(flow.get('SourcePort', 0)),
        float(flow.get('DestinationPort', 0)),
        1.0 if flow.get('Protocol', '').upper() == 'TCP' else 2.0 if flow.get('Protocol', '').upper() == 'UDP' else 0.0,
        float(flow.get('BytesSent', 0)),
        float(flow.get('BytesReceived', 0)),
        float(flow.get('PacketsSent', 0)),
        float(flow.get('PacketsReceived', 0)),
        float(flow.get('EndTime', 0)) - float(flow.get('StartTime', 0)),
    ]
    is_anomaly, loss = predict(input_features, MODEL_PATH, THRESHOLD)
    print(f"[REAL-TIME] Flow {flow_key} | Anomaly={is_anomaly} | Loss={loss} | Features={input_features}")

def main():
    #print("Starting real-time anomaly detection...")
    capture_flows(interface='Wi-Fi', display=False, max_packets=None, on_new_flow=on_flow_update)

if __name__ == "__main__":
    main()
