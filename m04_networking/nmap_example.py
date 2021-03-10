from nmap import PortScanner, PortScannerAsync
from pprint import pprint

nm = PortScanner()

while True:

    ip = input("\nInput IP address to scan: ")
    if not ip:
        break

    print(f"\n--- beginning scan of {ip}")
    output = nm.scan(ip, '22-1024', arguments="-sS -sU -O --host-time 600")
    print(f"--- --- command: {nm.command_line()}")

    print("----- nmap scan output -------------------")
    pprint(output)

    # DEMYSTIFYING TREATING CLASS LIKE DICT
    scan_output_1 = nm[ip]  # 'nm' is a class - why can you do this? __getitem__ in PortScanner
    scan_output_2 = nm._scan_result['scan'][ip]  # this is what __getitem__ returns
    print(f"\nScan output reference comparison: {scan_output_2==scan_output_1}\n")

    try:
        pprint(nm[ip].all_tcp())
        pprint(nm[ip].all_udp())
        pprint(nm[ip].all_ip())
    except KeyError as e:
        print(f"   ---> failed to get scan results for {ip}")

    print(f"--- end scan of {ip}")

print("\nExiting nmap scanner")

# print("\nScanning all hosts in subnet using port 22")
# nm.scan("192.168.254.0/24", arguments="-p 22 --open")
# print("--- iterating hosts with open port 22 (ssh)")
# for host in nm.all_hosts():
#     print("--- --- ", host)
#
# print("\nScanning all hosts in subnet using port 80")
# nm.scan("192.168.254.0/24", arguments="-p 80 --open")
# print("--- iterating hosts with open port 80 (http)")
# for host in nm.all_hosts():
#     print("--- --- ", host)

print("\nScanning all hosts in subnet using ICMP")
nm.scan("192.168.254.0/24", arguments="-PE")
print("--- iterating hosts responding to ICMP echo")
for host in nm.all_hosts():
    print("--- --- ", host)


def discovered_host(found_host, scan_result):
    if scan_result['nmap']['scanstats']['uphosts'] == '1':
        print(f"--- --- found host: {found_host} scan: {scan_result['nmap']['scanstats']}")


nma = PortScannerAsync()
print("\nScanning all hosts in subnet using ICMP with callback")
nma.scan("192.168.254.0/24", arguments="-PE", callback=discovered_host)
print("--- iterating hosts responding to ICMP echo")
while nma.still_scanning():
    nma.wait(5)
