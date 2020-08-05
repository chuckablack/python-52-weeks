import pyshark

capture = pyshark.LiveCapture(interface='enp0s3', only_summaries=True, bpf_filter='host 192.168.254.14 and not arp')
# capture.sniff(packet_count=100)

for packet in capture.sniff_continuously():
    print(packet)

# cap = pyshark.LiveCapture(interface='enp0s3')

# def print_conversation_header(pkt):
#     try:
#         protocol =  pkt.transport_layer
#         src_addr = pkt.ip.src
#         src_port = pkt[pkt.transport_layer].srcport
#         dst_addr = pkt.ip.dst
#         dst_port = pkt[pkt.transport_layer].dstport
#         print('%s  %s:%s --> %s:%s' % (protocol, src_addr, src_port, dst_addr, dst_port))
#     except AttributeError as e:
#         #ignore packets that aren't TCP/UDP or IPv4
#         pass
#
# cap.apply_on_packets(print_conversation_header, timeout=100)