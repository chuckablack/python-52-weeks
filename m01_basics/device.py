from pprint import pprint


# DICTIONARY representing a device
device = {
    "name": "r3-L-K2",
    "vendor": "cisco",
    "model": "catalyst-2690",
    "os": "iosxe",
    "version": "12.2SE",
    "ip": "10.1.1.1",
}

# SIMPLE PRINT
print(device)

# PRETTY PRINT
print()
pprint(device)

# FOR LOOP, NICELY FORMATTED PRINT
print()
for key, value in device.items():
    print(f"{key:>16s} : {value}")
