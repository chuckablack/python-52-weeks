import scapy.all as scapy
from tabulate import tabulate
import socket
from datetime import datetime
import requests
from operator import itemgetter


hosts = dict()

# DISCOVER HOSTS ON NETWORK USING ARPING FUNCTION
print(
    "\n\n----- Discovery hosts on network using arping() function ---------------------"
)
ans, unans = scapy.arping("192.168.254.0/24")
ans.summary()

for res in ans.res:
    print(f"---> IP address discovered: {res[0].payload.pdst}")

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
        "availability": True
    }

    # Dict and List point at same host data; doing list in order to use 'tabulate' easily
    hosts[host["hostname"]] = host

print("\n----- Hosts discovered (tabulate) --------------------")
print("\n", tabulate(sorted(hosts.values(),  key=itemgetter("hostname")), headers="keys"))

rsp = requests.post("http://127.0.0.1:5000/hosts", json=hosts)
if rsp.status_code != 204:
    print(
        f"{str(datetime.now())[:-3]}: Error posting to /hosts, response: {rsp.status_code}, {rsp.content}"
    )

response = requests.get("http://127.0.0.1:5000/hosts")
if response.status_code != 200:
    print(f"get hosts failed: {response.reason}")
    exit()

hosts_received = response.json()
# print("\n----- Hosts received from flask mini-quokka --------------------")
# pprint(hosts_received)

print("\n----- Compare hosts discovered with hosts retrieved from flask")
if hosts == hosts_received:
    print("\n     success! hosts discovered equals hosts retrieved")
else:
    print("\n     oops! hosts retrieved are not equal to what was discovered")

print("\n----- Hosts received (tabulate) --------------------")
print("\n", tabulate(sorted(hosts_received.values(),  key=itemgetter("hostname")), headers="keys"))
