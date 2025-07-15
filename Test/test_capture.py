import sys
import os
import struct
import socket
import psutil
import requests # type: ignore
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from NetworkTrafficCapture.Capture import capture_flows

def ip_to_int(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except Exception:
        return 0.0

def get_process_name(src_ip, src_port):
    try:
        for conn in psutil.net_connections(kind='inet'):
            laddr = conn.laddr if conn.laddr else None
            if laddr and laddr.ip == src_ip and laddr.port == src_port:
                try:
                    return psutil.Process(conn.pid).name()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return "Unknown"
    except Exception as e:
        print(f"[ERROR] Getting process name failed: {e}")
    return "Unknown"

def get_process_user(src_ip, src_port):
    try:
        for conn in psutil.net_connections(kind='inet'):
            laddr = conn.laddr if conn.laddr else None
            if laddr and laddr.ip == src_ip and laddr.port == src_port:
                try:
                    return psutil.Process(conn.pid).username()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return "Unknown"
    except Exception as e:
        print(f"[ERROR] Getting process user failed: {e}")
    return "Unknown"

def on_flow_update(flow_key, flow):
    # Extract values first
    src_ip = flow.get('SourceIP', '0.0.0.0')
    dest_ip = flow.get('DestinationIP', '0.0.0.0')
    src_port = int(flow.get('SourcePort', 0))
    dest_port = int(flow.get('DestinationPort', 0))
    protocol = flow.get('Protocol', '').upper()
    bytes_sent = int(flow.get('BytesSent', 0))
    bytes_received = int(flow.get('BytesReceived', 0))
    packets_sent = int(flow.get('PacketsSent', 0))
    packets_received = int(flow.get('PacketsReceived', 0))
    duration = float(flow.get('EndTime', 0)) - float(flow.get('StartTime', 0))
    process_name = get_process_name(src_ip, src_port)
    process_user = get_process_user(src_ip, src_port)

    # Only print if process_name is not "Unknown"
    if process_name != "Unknown":
        input_features = [
            src_ip,
            dest_ip,
            src_port,
            dest_port,
            protocol,
            bytes_sent,
            bytes_received,
            packets_sent,
            packets_received,
            duration,
            process_name,
            process_user
        ]
        print(f"[REAL-TIME] Features={input_features}")

def main():
    capture_flows(interface='Wi-Fi', display=False, max_packets=None, on_new_flow=on_flow_update)

if __name__ == "__main__":
    main()
