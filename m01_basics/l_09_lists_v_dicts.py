from util.create_utils import create_devices
from random import choice
import string
from tabulate import tabulate
import time


# --- Main program --------------------------------------------
if __name__ == '__main__':

    devices = create_devices(num_devices=254, num_subnets=254)

    # Create dictionary pointing at those same devices
    devices_dict = dict()
    for device in devices:
        devices_dict[device["ip"]] = device

    print("calculating tabular output of devices ...")
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
            continue

        start = time.time()
        if ip_to_find in devices_dict:
            print(f"---> found it (dict): {devices_dict[ip_to_find]}")
            dict_search_time = (time.time() - start) * 1000
            print(f"--- ---> in:  {dict_search_time} msec")
            print(f"--- ---> id of device:", id(devices_dict[ip_to_find]))

        print(f"conclusion: dictionary search was {int(list_search_time/dict_search_time)} times faster than list search")
