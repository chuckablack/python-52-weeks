device = {
    "name": "r3-L-n7",
    "vendor": "cisco",
    "model": "catalyst 2960",
    "os": "ios",
    "interfaces": [
    ]
}

print("\nDevice without interfaces")
for key, value in device.items():
    print(f"{key:>16s} : {value}")

interfaces = list()
for index in range(0, 8):
    interface = {
        "name": "g/0/0/" + str(index),
        "speed": "1000"
    }
    interfaces.append(interface)

device["interfaces"] = interfaces

print("\nDevice without interfaces")
for key, value in device.items():
    if key != "interfaces":
        print(f"{key:>16s} : {value}")
    else:
        print(f"{key:>16s} :")
        for interface in interfaces:
            print(f"\t\t\t\t\t{interface}")

from pprint import pprint
print()
pprint(device)

