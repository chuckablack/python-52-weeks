from random import choice
import string
from tabulate import tabulate
from operator import itemgetter
from enum import Enum

# CISCO = "cisco"
# JUNIPER = "juniper"
# ARISTA = "arista"


class Vendor(Enum):
    CISCO = "cisco"
    JUNIPER = "juniper"
    ARISTA = "arista"


# class Vendor:
#     CISCO = "cisco"
#     JUNIPER = "juniper"
#     ARISTA = "arista"


# class Vendor(Enum):
#     CISCO = 1
#     JUNIPER = 2
#     ARISTA = 3


devices = list()   # CREATE EMPTY LIST FOR HOLDING DEVICES

# FOR LOOP TO CREATE LARGE NUMBER OF DEVICES
for index in range(20):

    # CREATE DEVICE DICTIONARY
    device = dict()

    # RANDOM DEVICE NAME
    device["name"] = (
        choice(["r2", "r3", "r4", "r6", "r10"])
        + choice(["L", "U"])
        + choice(string.ascii_letters)
    )

    # RANDOM VENDOR FROM CHOICE OF CISCO, JUNIPER, ARISTA
    device["vendor"] = choice([Vendor.CISCO.value, Vendor.JUNIPER.value, Vendor.ARISTA.value])
    if device["vendor"] == Vendor.CISCO.value:
        device["os"] = choice(["ios", "iosxe", "iosxr", "nexus"])
        device["version"] = choice(["12.1(T).04", "14.07X", "8.12(S).010", "20.45"])
    elif device["vendor"] == Vendor.JUNIPER.value:
        device["os"] = "junos"
        device["version"] = choice(["J6.23.1", "8.43.12", "6.45", "6.03"])
    elif device["vendor"] == Vendor.ARISTA.value:
        device["os"] = "eos"
        device["version"] = choice(["2.45", "2.55", "2.92.145", "3.01"])
    device["ip"] = "10.0.0." + str(index)

    # NICELY FORMATTED PRINT OF THIS ONE DEVICE
    print()
    for key, value in device.items():
        print(f"{key:>16s} : {value}")

    # ADD THIS DEVICE TO THE LIST OF DEVICES
    devices.append(device)

# USE 'TABULATE' TO PRINT TABLE OF DEVICES
print()
print(tabulate(sorted(devices, key=itemgetter("vendor", "os", "version")), headers="keys"))
