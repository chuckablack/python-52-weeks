import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, ICMP

# CAPTURE EVERYTHING AND PRINT PACKET SUMMARIES
print("\n----- Packet summaries --------------------")
capture = scapy.sniff(iface='enp0s3', count=10)
print(capture.nsummary())

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
print("\n\n----- Capture and print packets as sniffed ---------------------")


def print_packet(pkt):
    print("    ", pkt.summary())


scapy.sniff(iface='enp0s3', prn=print_packet, filter="tcp port https", count=10)


# CAPTURE AND HANDLE PACKETS AS THEY ARRIVE USing LAMBDA
print("\n\n----- Capture and print packets as sniffed (using lambda) ---------------------")
scapy.sniff(iface='enp0s3', prn=lambda pkt: print(f"lambda    {pkt.summary()}"), filter="tcp port https", count=10)

# DISCOVER HOSTS ON NETWORKING USING MANUAL ARP PING
print("\n\n----- Discovery hosts on network using manual ARP ping ---------------------")
ans, unans = scapy.srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.254.0/24"), timeout=2)
ans.summary()

# DISCOVER HOSTS ON NETWORKING USING ARP PING FUNCTION
print("\n\n----- Discovery hosts on network using  ARP ping function ---------------------")
ans, unans = scapy.arping("192.168.254.0/24")
ans.summary()

for res in ans.res:
    print(f"---> IP address discovered: {res[0].payload.pdst}")

# DISCOVER HOSTS ON NETWORKING USING ICMP PING
# print("\n\n----- Discovery hosts on network using ICMP ping ---------------------")
# ans, unans = scapy.sr(IP(dst="192.168.254.1-254")/ICMP(), iface='enp0s3')
# print("Done???")
# ans.summary()

