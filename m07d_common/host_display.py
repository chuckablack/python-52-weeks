import os
import subprocess
import sys
from time import sleep
from colorama import Fore

import requests
from quokka_constants import DISPLAY_WAIT_TIME


def get_hosts():

    response = requests.get("http://127.0.0.1:5001/hosts")
    if response.status_code != 200:
        print(f"get hosts failed: {response.reason}")
        return {}

    return response.json()


def set_missing_fields(host):

    for fieldname in ["hostname", "ip_address", "mac_address", "availability", "last_heard", "open_tcp_ports"]:
        if fieldname not in host:
            host[fieldname] = ""


def print_hosts(hosts, previous_hosts):

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(
        "\n  __Hostname______________     ___IP_address___   ___MAC_address___   "
        + "__Avail__   __Last_Heard___________   __Open_TCP_Ports_____\n"
    )
    for host in hosts.values():

        set_missing_fields(host)

        if not host["availability"]:
            color = Fore.RED
        elif host["hostname"] in previous_hosts and host == previous_hosts[host["hostname"]]:
            color = Fore.GREEN
        else:
            color = Fore.LIGHTGREEN_EX

        print(
            color +
            f"  {host['hostname'][:26]:<26}"
            + f"   {host['ip_address']:<16}"
            + f"   {host['mac_address']:>17}"
            + f"   {str(host['availability']):>7}  "
            + f"   {host['last_heard']:>16}"
            + f"   {host['open_tcp_ports']}"
            + Fore.WHITE
        )

    print()
    for remaining in range(DISPLAY_WAIT_TIME, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"  Refresh: {remaining:3d} seconds remaining.")
        sys.stdout.flush()
        sleep(1)

    print("   ... retrieving hosts ...")


def main():

    previous_hosts = dict()
    while True:
        hosts = get_hosts()
        print_hosts(hosts, previous_hosts)
        previous_hosts = hosts


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting host-display")
        exit()
