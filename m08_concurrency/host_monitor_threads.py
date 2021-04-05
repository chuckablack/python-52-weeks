import subprocess
import threading
from datetime import datetime
from time import time

from hosts_common import discovery, get_hosts


def ping_host(host):

    try:
        subprocess.check_output(
            ["ping", "-c3", "-n", "-i0.5", "-W2", host["ip_address"]]
        )
        host["availability"] = True
        host["last_heard"] = str(datetime.now())[:-3]
        print(f"----> Host ping successful: {host['hostname']}")

    except subprocess.CalledProcessError:
        host["availability"] = False
        print(f" !!!  Host ping failed: {host['hostname']}")


def main():

    # discovery()

    hosts = get_hosts()
    print(f"\n---> Starting to ping {len(hosts)} hosts using threads")

    time_start = time()

    # ----- PING USING THREADS --------------------
    ping_host_threads = list()
    for host in hosts.values():
        ping_thread = threading.Thread(target=ping_host, args=(host,))
        ping_host_threads.append(ping_thread)
        ping_thread.start()

    for thread in ping_host_threads:
        thread.join()

    ping_with_threads_time = time() - time_start
    print(f"---> Completed pinging {len(hosts)} hosts using threads, time:", ping_with_threads_time)

    # ----- PING ONE AT A TIME --------------------
    print(f"\n---> Starting to ping {len(hosts)} hosts NOT using threads")
    time_start = time()

    for host in hosts.values():
        ping_host(host)

    ping_without_threads_time = time() - time_start
    print(f"---> Completed pinging {len(hosts)} hosts NOT using threads, time:", ping_without_threads_time)

    print("\nResults:")
    print(f"     Using threads:     {ping_with_threads_time}")
    print(f"     Not using threads: {ping_without_threads_time}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting host-monitor")
        exit()
