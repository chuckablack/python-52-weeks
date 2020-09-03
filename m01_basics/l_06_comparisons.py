from l_03_functions import create_devices
from pprint import pprint

devices = create_devices(num_subnets=2, num_devices=25)
print("   NAME      VENDOR : OS      IP ADDRESS       VERSION")
print("  -----     -------   -----   --------------   -----------")
for device in devices:
    print(
        f'{device["name"]:>7}  {device["vendor"]:>10} : {device["os"]:<6}  {device["ip"]:<15}  {device["version"]}'
    )

print("\n----- Starting comparison of device names --------------------")
for index, device_a in enumerate(devices):
    for device_b in devices[index:]:
        if device_a["ip"] == device_b["ip"]:
            continue
        if device_a["name"] == device_b["name"]:
            print(f"Found match! {device_a['name']} for both {device_a['ip']} and {device_b['ip']}")
print("----- Comparison of device names completed")

print("\n----- Create table of arbitrary 'standard' versions for each vendor:os --------------------")
standard_versions = dict()
for device in devices:
    vendor_os = device["vendor"] + ":" + device["os"]
    if vendor_os not in standard_versions:
        standard_versions[vendor_os] = device["version"]
pprint(standard_versions)

print("\n----- Create list of non-compliant devices for each vendor:os --------------------")
non_compliant_devices = dict()
for vendor_os, _ in standard_versions.items():
    non_compliant_devices[vendor_os] = []

for device in devices:
    vendor_os = device["vendor"] + ":" + device["os"]
    if device["version"] != standard_versions[vendor_os]:
        non_compliant_devices[vendor_os].append(device["ip"] + " version: " + device["version"])

pprint(non_compliant_devices)
