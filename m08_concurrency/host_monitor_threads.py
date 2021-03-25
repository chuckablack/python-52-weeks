import subprocess
from datetime import datetime, timedelta
from time import sleep, time
import socket
import requests
import scapy.all as scapy
import threading

MONITOR_INTERVAL = 15
DISCOVERY_INTERVAL = 300


def get_hosts():

    print("\n\n----> Retrieving hosts ...", end="")
    response = requests.get("http://127.0.0.1:5001/hosts")
    if response.status_code != 200:
        print(f" !!!  Failed to retrieve hosts from server: {response.reason}")
        return {}

    print(" Hosts successfully retrieved")
    return response.json()


# def discovery():
#
#     # DISCOVER HOSTS ON NETWORK USING ARPING FUNCTION
#     print(
#         "\n\n----- Discovery hosts on network using arping() function ---------------------"
#     )
#     ans, unans = scapy.arping("192.168.254.0/24")
#     ans.summary()
#
#     for res in ans.res:
#         print(f"oooo> IP address discovered: {res[0].payload.pdst}")
#
#         ip_addr = res[1].payload.psrc
#         mac_addr = res[1].payload.hwsrc
#         try:
#             hostname = socket.gethostbyaddr(str(ip_addr))
#         except (socket.error, socket.gaierror):
#             hostname = (str(ip_addr), [], [str(ip_addr)])
#         last_heard = str(datetime.now())[:-3]
#
#         host = {
#             "ip_address": ip_addr,
#             "mac_address": mac_addr,
#             "hostname": hostname[0],
#             "last_heard": last_heard,
#             "availability": True
#         }
#         update_host(host)


# def update_host(host):
#
#     print(f"----> Updating host status via REST API: {host['hostname']}", end="")
#     rsp = requests.put("http://127.0.0.1:5001/hosts", params={"hostname": host["hostname"]}, json=host)
#     if rsp.status_code != 204:
#         print(
#             f"{str(datetime.now())[:-3]}: Error posting to /hosts, response: {rsp.status_code}, {rsp.content}"
#         )
#         print(f" !!!  Unsuccessful attempt to update host status via REST API: {host['hostname']}")
#     else:
#         print(f" Successfully updated host status via REST API: {host['hostname']}")


def ping_host(host):

    try:
        print(f"----> Pinging host: {host['hostname']}", end="")
        subprocess.check_output(
            ["ping", "-c3", "-n", "-i0.5", "-W2", host["ip_address"]]
        )
        host["availability"] = True
        host["last_heard"] = str(datetime.now())[:-3]
        print(f" Host ping successful: {host['hostname']}")

    except subprocess.CalledProcessError:
        host["availability"] = False
        print(f" !!!  Host ping failed: {host['hostname']}")


def main():

    # last_discovery = datetime.now()-timedelta(days=1)

    while True:

        # if (datetime.now() - last_discovery).total_seconds() > DISCOVERY_INTERVAL:
        #     discovery()
        #     last_discovery = datetime.now()

        hosts = get_hosts()
        print(f"\n---> Starting to ping {len(hosts)} hosts using threads")

        ping_host_threads = list()
        time_start = time()

        for host in hosts.values():
            ping_thread = threading.Thread(target=ping_host, args=(host,))
            ping_host_threads.append(ping_thread)
            ping_thread.start()

        for thread in ping_host_threads:
            thread.join()

        ping_with_threads_time = time() - time_start
        print(f"---> Completed pinging {len(hosts)} hosts using threads, time:", ping_with_threads_time)

        # for host in hosts.values():
        #     update_host(host)

        print(f"\n---> Starting to ping {len(hosts)} hosts NOT using threads")
        time_start = time()

        for host in hosts.values():
            ping_host(host)

        ping_without_threads_time = time() - time_start
        print(f"---> Completed pinging {len(hosts)} hosts NOT using threads, time:", ping_without_threads_time)

        print("\nResults:")
        print(f"     Using threads:     {ping_with_threads_time}")
        print(f"     Not using threads: {ping_without_threads_time}\n")

        sleep(MONITOR_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting host-monitor")
        exit()
