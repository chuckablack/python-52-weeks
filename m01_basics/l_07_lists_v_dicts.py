from random import choice
import string
from tabulate import tabulate
import time


def create_devices(num_devices=1, num_subnets=1):

    # CREATE LIST OF DEVICES
    created_devices = list()
    created_devices_dict = dict()

    if num_devices > 254 or num_subnets > 254:
        print("Error: too many devices and/or subnets requested")
        return created_devices

    for subnet_index in range(1, num_subnets+1):

        for device_index in range(1, num_devices+1):

            # CREATE DEVICE DICTIONARY
            device = dict()

            # RANDOM DEVICE NAME
            device["name"] = (
                    choice(["r2", "r3", "r4", "r6", "r10"])
                    + choice(["L", "U"])
                    + choice(string.ascii_letters)
            )

            # RANDOM VENDOR FROM CHOICE OF CISCO, JUNIPER, ARISTA
            device["vendor"] = choice(["cisco", "juniper", "arista"])
            if device["vendor"] == "cisco":
                device["os"] = choice(["ios", "iosxe", "iosxr", "nexus"])
                device["version"] = choice(["12.1(T).04", "14.07X", "8.12(S).010", "20.45"])
            elif device["vendor"] == "juniper":
                device["os"] = "junos"
                device["version"] = choice(["12.3R12-S15", "15.1R7-S6", "18.4R2-S3", "15.1X53-D591"])
            elif device["vendor"] == "arista":
                device["os"] = "eos"
                device["version"] = choice(["4.24.1F", "4.23.2F", "4.22.1F", "4.21.3F"])

            device["ip"] = "10.0." + str(subnet_index) + "." + str(device_index)

            created_devices.append(device)
            created_devices_dict[device["ip"]] = device

    return created_devices, created_devices_dict


# --- Main program --------------------------------------------
if __name__ == '__main__':

    devices, devices_dict = create_devices(num_devices=254, num_subnets=254)
    print("\n", tabulate(devices, headers="keys"))

    while True:

        ip_to_find = input("\nEnter IP address to find: ")
        if not ip_to_find:
            break

        start = time.time()
        for device in devices:
            if device["ip"] == ip_to_find:
                print(f"---> found it (list): {device}")
                list_search_time = (time.time() - start) * 1000
                print(f"--- ---> in:  {list_search_time} msec")
                print(f"--- ---> id of device:", id(device))
                break
        else:
            print(f"---! IP address not found, try again")
            break

        start = time.time()
        if ip_to_find in devices_dict:
            print(f"---> found it (dict): {devices_dict[ip_to_find]}")
            dict_search_time = (time.time() - start) * 1000
            print(f"--- ---> in:  {dict_search_time} msec")
            print(f"--- ---> id of device:", id(devices_dict[ip_to_find]))

        print(f"conclusion: dictionary search was {int(list_search_time/dict_search_time)} faster than list search")
