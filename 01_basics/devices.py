from random import choice
import string
from tabulate import tabulate
from operator import itemgetter

devices = list()
for index in range(100):
    device = dict()
    device["name"] = (
        choice(["r2", "r3", "r4", "r6", "r10"])
        + choice(["L", "U"])
        + choice(string.ascii_letters)
    )
    device["vendor"] = choice(["cisco", "juniper", "arista"])
    if device["vendor"] == "cisco":
        device["os"] = choice(["ios", "iosxe", "iosxr", "nexus"])
        device["version"] = choice(["12.1(T).04", "14.07X", "8.12(S).010", "20.45"])
    elif device["vendor"] == "juniper":
        device["os"] = "junos"
        device["version"] = choice(["J6.23.1", "8.43.12", "6.45", "6.03"])
    elif device["vendor"] == "arista":
        device["os"] = "eos"
        device["version"] = choice(["2.45", "2.55", "2.92.145", "3.01"])
    device["ip"] = "10.0.0." + str(index)

    print()
    for key, value in device.items():
        print(f"{key:>16s} : {value}")

    devices.append(device)

print()
print(tabulate(sorted(devices, key=itemgetter("vendor", "os", "version")), headers="keys"))
