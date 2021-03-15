import requests
import json
import subprocess
import os
import sys
from time import sleep
from signal import signal, SIGINT


def exit_gracefully(signal_received, frame):
    print("\n\nexiting gracefully")
    exit(0)


signal(SIGINT, exit_gracefully)

while True:

    query_params = {
        "device": "ios-xe-mgmt.cisco.com",
        "type": "csr",
        "port": "8181",
        "username": "developer",
        "password": "C1sco12345",
    }
    response = requests.get(
        "http://127.0.0.1:5000/interface_counters", params=query_params
    )
    if response.status_code != 200:
        print(f"get interface counters failed: {response.reason}")
        exit()

    counters = response.json()
    print(json.dumps(counters, indent=4))

    intf_counters_list = sorted([(k, v) for k, v in counters.items()])

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(
        "__Name________________     __Rx Packets__   _____Rx Octets__   __Tx Packets__   _____Tx Octets__"
    )
    for intf_name, intf_counters in intf_counters_list:
        if (
            "rx_unicast_packets" in intf_counters
            and "rx_octets" in intf_counters
            and "tx_unicast_packets" in intf_counters
            and "tx_octets" in intf_counters
        ):
            print(
                f"  {intf_name:<20}"
                + f"   {intf_counters['rx_unicast_packets']:>14}"
                + f"   {intf_counters['rx_octets']:>16}"
                + f"   {intf_counters['tx_unicast_packets']:>14}"
                + f"   {intf_counters['tx_octets']:>16}"
            )

    print("\n\n")
    for remaining in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"Refresh: {remaining:2d} seconds remaining.")
        sys.stdout.flush()
        sleep(1)

    print("   ... updating counters ...")
