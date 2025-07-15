import pyshark
import time

def capture_flows(interface='Wi-Fi', display=True, max_packets=None, on_new_flow=None):
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
                    rev_flow_key = (dst_ip, src_ip, dst_port, src_port, protocol)  # Reverse flow

                    # Initialize forward flow if not present
                    if flow_key not in flows:
                        flows[flow_key] = {
                            'SourceIP': src_ip,
                            'DestinationIP': dst_ip,
                            'SourcePort': int(src_port),
                            'DestinationPort': int(dst_port),
                            'Protocol': protocol,
                            'BytesSent': 0,
                            'BytesReceived': 0,
                            'PacketsSent': 0,
                            'PacketsReceived': 0,
                            'StartTime': now,
                            'EndTime': now
                        }
                    # Initialize reverse flow if not present
                    if rev_flow_key not in flows:
                        flows[rev_flow_key] = {
                            'SourceIP': dst_ip,
                            'DestinationIP': src_ip,
                            'SourcePort': int(dst_port),
                            'DestinationPort': int(src_port),
                            'Protocol': protocol,
                            'BytesSent': 0,
                            'BytesReceived': 0,
                            'PacketsSent': 0,
                            'PacketsReceived': 0,
                            'StartTime': now,
                            'EndTime': now
                        }

                    # Update forward flow (sent)
                    flows[flow_key]['BytesSent'] += length
                    flows[flow_key]['PacketsSent'] += 1
                    flows[flow_key]['EndTime'] = now

                    # Update reverse flow (received)
                    flows[rev_flow_key]['BytesReceived'] += length
                    flows[rev_flow_key]['PacketsReceived'] += 1
                    flows[rev_flow_key]['EndTime'] = now

                    if on_new_flow is not None:
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
