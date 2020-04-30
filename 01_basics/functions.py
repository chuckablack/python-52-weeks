from random import choice
import string
from tabulate import tabulate


def create_devices(num_devices=100):

    # CREATE LIST OF DEVICES
    created_devices = list()

    if num_devices > 254:
        print("Error: too many devices requested")
        return created_devices

    for index in range(num_devices):

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
            device["version"] = choice(["J6.23.1", "8.43.12", "6.45", "6.03"])
        elif device["vendor"] == "arista":
            device["os"] = "aos"
            device["version"] = choice(["2.45", "2.55", "2.92.145", "3.01"])

        device["ip"] = "10.0.0." + str(index)

        created_devices.append(device)

    return created_devices


# --- Main program --------------------------------------------
devices = create_devices(20)
print("\n", tabulate(devices, headers="keys"))
