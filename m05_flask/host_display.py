import os
import subprocess
import sys
from time import sleep
import colorama
from colorama import Fore

import requests


def get_hosts():

    response = requests.get("http://127.0.0.1:5000/hosts")
    if response.status_code != 200:
        print(f"get hosts failed: {response.reason}")
        return {}

    return response.json()


def print_hosts(hosts, previous_hosts):

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(
        "\n  __Hostname______________     ___IP_address___   ___MAC_address___   __Avail__   __Last_Heard___________\n"
    )
    for host in hosts.values():

        if host["hostname"] in previous_hosts and host == previous_hosts[host["hostname"]]:
            color = Fore.GREEN
        else:
            color = Fore.RED

        print(
            color +
            f"  {host['hostname'][:26]:<26}"
            + f"   {host['ip']:<16}"
            + f"   {host['mac']:>17}"
            + f"   {str(host['availability']):>7}  "
            + f"   {host['last_heard']:>16}"
            + Fore.WHITE
        )

    print("\n\n")
    for remaining in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"Refresh: {remaining:3d} seconds remaining.")
        sys.stdout.flush()
        sleep(1)

    print("   ... retrieving hosts ...")


previous_hosts = dict()
while True:
    try:
        hosts = get_hosts()
        print_hosts(hosts, previous_hosts)
        previous_hosts = hosts

    except KeyboardInterrupt:
        print("\n\n---> Exiting host display")
        exit()
