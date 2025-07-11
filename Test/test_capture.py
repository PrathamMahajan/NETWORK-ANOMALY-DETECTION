import sys
import os
import struct
import socket
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from NetworkTrafficCapture.Capture import capture_flows

def ip_to_int(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except Exception:
        return 0.0

def on_flow_update(flow_key, flow):
    #Convert flow dict to feature vector in required order
    input_features = [
        flow.get('SourceIP', '0.0.0.0'),
        flow.get('DestinationIP', '0.0.0.0'),
        int(flow.get('SourcePort', 0)),
        int(flow.get('DestinationPort', 0)),
        1.0 if flow.get('Protocol', '').upper() == 'TCP' else 2.0 if flow.get('Protocol', '').upper() == 'UDP' else 0.0,
        int(flow.get('BytesSent', 0)),
        int(flow.get('BytesReceived', 0)),
        int(flow.get('PacketsSent', 0)),
        int(flow.get('PacketsReceived', 0)),
        float(flow.get('EndTime', 0)) - float(flow.get('StartTime', 0)),
    ]
    print(f"[REAL-TIME] Features={input_features}")


def main():
    capture_flows(interface='Wi-Fi', display=False, max_packets=None, on_new_flow=on_flow_update)

if __name__ == "__main__":
    main()