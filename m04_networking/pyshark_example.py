import pyshark

# CAPTURE EVERYTHING AND PRINT PACKET SUMMARIES
print("\n----- Packet summaries --------------------")
capture = pyshark.LiveCapture(interface='enp0s3', only_summaries=True)
capture.sniff(packet_count=10)
for packet in capture:
    print(f"    {packet}")

# CAPTURE DNS AND PRINT PACKETS
print("\n----- DNS packet summaries (collect for 50 packets) --------------------")
capture = pyshark.LiveCapture(interface='enp0s3', only_summaries=True, display_filter='dns')
capture.sniff(packet_count=50)
for packet in capture:
    print(f"    {packet}")

# CAPTURE ONLY DNS AND PRINT COMPLETE PACKETS
print("\n\n----- DNS packets, complete (collect for 40 total packets) ---------------------")
capture = pyshark.LiveCapture(interface='enp0s3', display_filter='dns')
capture.sniff(packet_count=40)
for packet in capture:
    print(packet)

# CAPTURE AND HANDLE PACKETS AS THEY ARRIVE
print("\n\n----- Print packets as they are detected to/from specified host ---------------------")
capture = pyshark.LiveCapture(interface='enp0s3', only_summaries=True, bpf_filter='tcp port https')


def print_packet(pkt):
    print("    ", pkt)


capture.apply_on_packets(print_packet, packet_count=20)
