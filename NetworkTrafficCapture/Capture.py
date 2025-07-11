import pyshark
import time

def capture_flows(interface='Wi-Fi', display=True, max_packets=None, on_new_flow=None):
    """
    Capture real-time network flows using pyshark.
    Args:
        interface (str): Network interface to capture on (e.g., 'Wi-Fi', 'Ethernet').
        display (bool): Whether to print flow info in real time.
        max_packets (int or None): Stop after this many packets (None for infinite).
        on_new_flow (function): Callback invoked with (flow_key, flow_dict) when a flow is updated.
    Returns:
        dict: Dictionary of flow statistics.
    """
    print(f"Starting real-time packet capture on interface '{interface}' with pyshark... Press Ctrl+C to stop.")
    cap = pyshark.LiveCapture(interface=interface)
    flows = {}
    packet_count = 0

    try:
        for pkt in cap.sniff_continuously():
            if max_packets is not None and packet_count >= max_packets:
                break
            try:
                if hasattr(pkt, 'ip'):
                    src_ip = pkt.ip.src
                    dst_ip = pkt.ip.dst
                    protocol = pkt.transport_layer if hasattr(pkt, 'transport_layer') else 'N/A'
                    src_port = pkt[pkt.transport_layer].srcport if protocol in ['TCP', 'UDP'] else '0'
                    dst_port = pkt[pkt.transport_layer].dstport if protocol in ['TCP', 'UDP'] else '0'
                    length = int(pkt.length)
                    now = time.time()

                    flow_key = (src_ip, dst_ip, src_port, dst_port, protocol)
                    if flow_key not in flows:
                        flows[flow_key] = {
                            'SourceIP': src_ip,
                            'DestinationIP': dst_ip,
                            'SourcePort': int(src_port),
                            'DestinationPort': int(dst_port),
                            'Protocol': protocol,
                            'BytesSent': 0,
                            'BytesReceived': 0,      # You may need to implement logic for this
                            'PacketsSent': 0,
                            'PacketsReceived': 0,    # You may need to implement logic for this
                            'StartTime': now,
                            'EndTime': now
                        }
                    flows[flow_key]['BytesSent'] += length
                    flows[flow_key]['PacketsSent'] += 1
                    flows[flow_key]['EndTime'] = now
                    # Optionally update BytesReceived/PacketsReceived for reverse flows

                    # Call the callback for real-time prediction
                    if on_new_flow is not None:
                        #print(f"[DEBUG] Calling on_new_flow for {flow_key}")
                        on_new_flow(flow_key, flows[flow_key])

                    if display:
                        print(f"Flow {flow_key}: {flows[flow_key]}")

                    packet_count += 1
            except Exception as e:
                pass  # Optionally log errors

    except KeyboardInterrupt:
        print("Packet capture manually interrupted.")

    finally:
        cap.close()
        return flows
