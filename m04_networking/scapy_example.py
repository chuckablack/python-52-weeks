import scapy.all as scapy

# CAPTURE EVERYTHING AND PRINT PACKET SUMMARIES
# print("\n----- Packet summaries --------------------")
# capture = scapy.sniff(iface='enp0s3', count=10)
# print(capture.nsummary())

# CAPTURE DNS AND PRINT PACKETS
print("\n----- DNS packet summaries (collect 10 DNS packets) --------------------")
capture = scapy.sniff(iface='enp0s3', filter="udp port 53", count=10)
print(capture.nsummary())

# CAPTURE ONLY DNS AND PRINT COMPLETE PACKETS
print("\n\n----- DNS packets, complete (collect 10 DNS packets) ---------------------")
capture = scapy.sniff(iface='enp0s3', filter="udp port 53", count=10)
for packet in capture:
    print(packet.show())


# CAPTURE AND HANDLE PACKETS AS THEY ARRIVE
def print_packet(pkt):
    print("    ", pkt.show())


scapy.sniff(iface='enp0s3', prn=print_packet, filter="tcp port https", count=10)
