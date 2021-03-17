import os
import subprocess
import sys
from time import sleep
from colorama import Fore

import requests
import re


def get_devices():

    response = requests.get("http://127.0.0.1:5000/devices")
    if response.status_code != 200:
        print(f"get devices failed: {response.reason}")
        return {}

    return response.json()


def print_devices(devices, previous_devices):

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(
        "\n  __Device_Name___________   ___IP_address___  ______Model_____ "
        + " _Version_ _Avail_ __Rsp_  __Last_Heard___________\n"
    )
    for device in devices.values():

        if not device["availability"]:
            color = Fore.RED
        elif device["name"] in previous_devices and device == previous_devices[device["name"]]:
            color = Fore.GREEN
        else:
            color = Fore.LIGHTGREEN_EX

        print(
            color +
            f"  {device['hostname'][:26]:<24}"
            + f"  {device['ip_address']:>16}"
            + f"   {device['model'][:16]:<16}"
            + f"   {device['os_version']:>7}"
            + f"   {str(device['availability']):>5}"
            + f"   {device['response_time']:>5.2f}"
            + f"  {device['last_heard']:>16}"
            + Fore.WHITE
        )

    print("\n\n")
    for remaining in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"  Refresh: {remaining:3d} seconds remaining.")
        sys.stdout.flush()
        sleep(1)

    print("   ... retrieving devices ...")


def main():

    previous_devices = dict()
    while True:
        devices = get_devices()
        print_devices(devices, previous_devices)
        previous_devices = devices


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting device-display")
        exit()
