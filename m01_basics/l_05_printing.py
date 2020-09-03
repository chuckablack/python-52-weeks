from l_03_functions import create_devices
from pprint import pprint
from operator import itemgetter
from tabulate import tabulate
from datetime import datetime
from time import sleep
from random import choice

devices = create_devices(25)

print("\n\nUSING PRINT")
print(devices)

print("\n\nUSING PPRINT")
pprint(devices)

print("\n\nUSING LOOP")
for device in devices:
    sleep(0.1)
    device["last_heard"] = str(datetime.now())
    print(device)

print("\n\nUSING TABULATE")
print(
    tabulate(sorted(devices, key=itemgetter("vendor", "os", "version")), headers="keys")
)

print("\n\nUSING LOOP AND F-STRING")
print("   NAME      VENDOR : OS      IP ADDRESS       LAST HEARD")
print("  -----     -------   -----   --------------   ----------------------")
for device in devices:
    print(
        f'{device["name"]:>7}  {device["vendor"]:>10} : {device["os"]:<6}  {device["ip"]:<15}  {device["last_heard"][:-4]}'
    )

print("\nSame thing, but sorted descending by last_heard")
for device in sorted(devices, key=itemgetter("last_heard"), reverse=True):
    print(
        f'{device["name"]:>7}  {device["vendor"]:>10} : {device["os"]:<6}  {device["ip"]:<15}  {device["last_heard"][:-4]}'
    )

print("\n\nMULTIPLE PRINT STATEMENTS, SAME LINE")
print("Testing Devices:")
for device in devices:
    print(f"--- testing device {device['name']} ... ", end="")
    sleep(choice([0.1, 0.2, 0.3, 0.4]))
    print("done.")
print("Testing completed")
