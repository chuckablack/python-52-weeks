import scapy.all as scapy
from scapy.layers.l2 import Ether, ARP
from scapy.layers.inet import IP, ICMP, TCP

# # CAPTURE EVERYTHING AND PRINT PACKET SUMMARIES
# print("\n----- Packet summaries --------------------")
# capture = scapy.sniff(iface='enp0s3', count=10)
# print(capture.nsummary())
#
# # CAPTURE DNS AND PRINT PACKETS
# print("\n----- DNS packet summaries (collect 10 DNS packets) --------------------")
# capture = scapy.sniff(iface='enp0s3', filter="udp port 53", count=10)
# print(capture.nsummary())
#
# # CAPTURE ONLY DNS AND PRINT COMPLETE PACKETS
# print("\n\n----- DNS packets, complete (collect 10 DNS packets) ---------------------")
# capture = scapy.sniff(iface='enp0s3', filter="udp port 53", count=10)
# for packet in capture:
#     print(packet.show())
#
#
# # CAPTURE AND HANDLE PACKETS AS THEY ARRIVE
# print("\n\n----- Capture and print packets as sniffed ---------------------")
#
#
# def print_packet(pkt):
#     print("    ", pkt.summary())
#
#
# scapy.sniff(iface='enp0s3', prn=print_packet, filter="tcp port https", count=10)
#
#
# # CAPTURE AND HANDLE PACKETS AS THEY ARRIVE USing LAMBDA
# print("\n\n----- Capture and print packets as sniffed (using lambda) ---------------------")
# scapy.sniff(iface='enp0s3', prn=lambda pkt: print(f"lambda    {pkt.summary()}"), filter="tcp port https", count=10)
#
# # DISCOVER HOSTS ON NETWORKING USING MANUAL ARP PING
# print("\n\n----- Discovery hosts on network using manual ARP ping ---------------------")
# ans, unans = scapy.srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.254.0/24"), timeout=2)
# ans.summary()
#
# # DISCOVER HOSTS ON NETWORKING USING ARP PING FUNCTION
# print("\n\n----- Discovery hosts on network using  ARP ping function ---------------------")
# ans, unans = scapy.arping("192.168.254.0/24")
# ans.summary()
#
# for res in ans.res:
#     print(f"---> IP address discovered: {res[0].payload.pdst}")
#
# # DISCOVER HOSTS ON NETWORKING USING ICMP PING
# # print("\n\n----- Discovery hosts on network using ICMP ping ---------------------")
# # ans, unans = scapy.sr(IP(dst="192.168.254.1-254")/ICMP(), timeout=1)
# # ans.summary()

# TCP PORT SCAN
print("\n\n----- See what ports are open on a device --------------------")
while True:

    ip = input("IP address on which to scan ports: ")
    if not ip:
        print("\n----- Ending port scanning")
        break

    # answers, unans = scapy.sr(IP(dst="192.168.254.254")/TCP(flags="S", sport=666, dport=[22, 80, 21, 443]), timeout=1)
    answers, unans = scapy.sr(IP(dst=ip)/TCP(flags="S", sport=666, dport=(1, 1024)), timeout=10)
    for answered in answers:
        print(f"---> open port: {answered[0].summary()}")

    print()
    for un_answered in unans:
        print(f"---> closed port: {un_answered[0].summary()}")

    print("\n----- Open/Closed port totals --------------------")
    print(f"\tOpen ports: {len(answers)}")
    print(f"\tClosed ports: {len(unans)}")

