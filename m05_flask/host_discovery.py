import scapy.all as scapy
from pprint import pprint
from tabulate import tabulate
import socket
from datetime import datetime
import requests


hosts_list = list()
hosts = dict()

# DISCOVER HOSTS ON NETWORK USING ARPING FUNCTION
print(
    "\n\n----- Discovery hosts on network using arping() function ---------------------"
)
ans, unans = scapy.arping("192.168.254.0/24")
ans.summary()

for res in ans.res:
    print(f"---> IP address discovered: {res[0].payload.pdst}")
    pprint(res)

    ip_addr = res[1].payload.psrc
    mac_addr = res[1].payload.hwsrc
    try:
        hostname = socket.gethostbyaddr(str(ip_addr))
    except (socket.error, socket.gaierror) as e:
        hostname = (str(ip_addr), [], [str(ip_addr)])
    last_heard = str(datetime.now())[:-3]

    host = {
        "ip": ip_addr,
        "mac": mac_addr,
        "hostname": hostname[0],
        "last_heard": last_heard,
    }

    # Dict and List point at same host data; doing list in order to use 'tabulate' easily
    hosts_list.append(host)
    hosts[host["hostname"]] = host

print("\n", tabulate(hosts_list, headers="keys"))

rsp = requests.post("http://127.0.0.1:5000/hosts", json=hosts)
if rsp.status_code != 200:
    print(
        f"{str(datetime.now())[:-3]}: Error calling /hosts response: {rsp.status_code}, {rsp.content}"
    )
