import napalm
import subprocess
import os
import sys
from time import sleep
from signal import signal, SIGINT


driver_csr = napalm.get_network_driver("ios")
driver_nxos = napalm.get_network_driver("nxos_ssh")

device_csr = driver_csr(
    hostname="ios-xe-mgmt-latest.cisco.com",
    username="developer",
    password="C1sco12345",
    optional_args={"port": 8181},
)
device_csr.open()

# device_nxos = driver_nxos(
#     hostname="sbx-nxos-mgmt.cisco.com",
#     username="admin",
#     password="Admin_1234!",
#     optional_args={"port": 8181},
# )
# device_nxos.open()


def exit_gracefully(signal_received, frame):
    print("\n\nexiting gracefully")
    exit(0)


signal(SIGINT, exit_gracefully)
while True:

    counters = device_csr.get_interfaces_counters()
    # print(json.dumps(counters, sort_keys=True, indent=4))

    intf_counters_list = sorted([(k, v) for k, v in counters.items()])

    subprocess.call("clear" if os.name == "posix" else "cls")
    print("__Name________________     __Rx Packets__   _____Rx Octets__   __Tx Packets__   _____Tx Octets__")
    for intf_name, intf_counters in intf_counters_list:
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

# counters_nxos = device_nxos.get_interfaces_ip()
# print(json.dumps(counters_nxos, sort_keys=True, indent=4))
