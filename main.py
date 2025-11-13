import sys
import os
import struct
import socket
import psutil
import requests # type: ignore
import time
import signal
from collections import defaultdict
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from NetworkTrafficCapture.Capture import capture_flows

WINDOW_SIZE = 20  # seconds
flow_buffer = []
window_start = time.time()
header_written = False
shutdown_requested = False

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

def aggregate_and_store(flows):
    file_path = 'Data.csv'
    file_exists = os.path.isfile(file_path)

    grouped = defaultdict(list)
    for flow in flows:
        key = (flow['src_ip'], flow['dest_ip'], flow['process_name'], flow['process_user'])
        grouped[key].append(flow)

    aggregated_data = []
    for key, group in grouped.items():
        total_bytes_sent = sum(f['bytes_sent'] for f in group)
        total_packets_sent = sum(f['packets_sent'] for f in group)
        total_duration = sum(f['duration'] for f in group)
        bytes_per_sec = total_bytes_sent / total_duration if total_duration else 0
        avg_packet_size = total_bytes_sent / total_packets_sent if total_packets_sent else 0
        unique_dest_ips = len(set(f['dest_ip'] for f in group))
        session_count = len(group)
        avg_duration = total_duration / session_count if session_count else 0

        record = {
            'src_ip': key[0],
            'dest_ip': key[1],
            'process_name': key[2],
            'process_user': key[3],
            'bytes_per_sec': bytes_per_sec,
            'avg_packet_size': avg_packet_size,
            'unique_dest_ips': unique_dest_ips,
            'session_count': session_count,
            'avg_duration': avg_duration,
            'window_end_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        }

        aggregated_data.append(record)

    if aggregated_data:
        try:
            df = pd.DataFrame(aggregated_data)
            df.to_csv(file_path, mode='a', header=not file_exists, index=False)
            print("[INFO] Flushed aggregated flow data to CSV.")
        except Exception as e:
            print(f"[ERROR] Failed to write to CSV: {e}")

def graceful_shutdown(signum, frame):
    global shutdown_requested
    print("\n[INFO] Graceful shutdown triggered.")
    shutdown_requested = True
    if flow_buffer:
        aggregate_and_store(flow_buffer)
        flow_buffer.clear()
    sys.exit(0)

def on_flow_update(flow_key, flow):
    global window_start, shutdown_requested
    if shutdown_requested:
        return

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
    last_packet_length = int(flow.get('LastPacketLength', 0))
    process_name = get_process_name(src_ip, src_port)
    process_user = get_process_user(src_ip, src_port)

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
            last_packet_length,
            process_name,
            process_user
        ]
        print(f"[REAL-TIME] Features={input_features}")

        flow_record = {
            'src_ip': src_ip,
            'dest_ip': dest_ip,
            'process_name': process_name,
            'process_user': process_user,
            'bytes_sent': bytes_sent,
            'packets_sent': packets_sent,
            'duration': duration
        }
        flow_buffer.append(flow_record)
        if time.time() - window_start >= WINDOW_SIZE:
            aggregate_and_store(flow_buffer)
            flow_buffer.clear()
            window_start = time.time()

def main():
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    print("[INFO] Starting real-time network traffic flow analyzer. Press Ctrl+C to stop.")
    capture_flows(interface='Wi-Fi', display=False, max_packets=None, on_new_flow=on_flow_update)

if __name__ == "__main__":
    main()
