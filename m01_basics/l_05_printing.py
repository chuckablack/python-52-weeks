from l_03_functions import create_devices
from pprint import pprint
from operator import itemgetter
from tabulate import tabulate

devices = create_devices(25)

print("\n\nUSING PRINT")
print(devices)

print("\n\nUSING PPRINT")
pprint(devices)

print("\n\nUSING LOOP")
for device in devices:
    print(device)

print("\n\nUSING TABULATE")
print(tabulate(sorted(devices, key=itemgetter("vendor", "os", "version")), headers="keys"))

print("\n\nUSING LOOP AND F-STRING")
print("        NAME      VENDOR  OS      IP ADDRESS")
print("       -----     -------  -----   -----------")
for device in devices:
    print(f'    {device["name"]:>8}  {device["vendor"]:>10}  {device["os"]:<6}  {device["ip"]:<15}')
