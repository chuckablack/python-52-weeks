from pprint import pprint


device = {
    "name": "r3-L-K2",
    "vendor": "cisco",
    "model": "catalyst-2690",
    "os": "iosxe",
    "version": "12.2SE",
    "ip": "10.1.1.1",
}

print(device)

print()
pprint(device)

print()
for key, value in device.items():
    print(f"{key:>16s} : {value}")
