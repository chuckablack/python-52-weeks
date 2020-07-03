device1_str = "  r3-L-n7, cisco, catalyst 2960, ios  "
device2_str = "  r3-U-n7, cisco, catalyst 2960, ios  "
device3_str = "r5-U-n7, juniper, mx10003, junos"
device4_str = "r5-L-n7, juniper, mx10003, junos"
device5_str = "r6-U-n7, arista, 720XP, eos"

# SPLIT
print("STRING STRIP, SPLIT, REPLACE")
device1 = device1_str.split(",")
print("device1 using split:", device1)

# STRIP
device1 = device1_str.strip().split(",")
print("device1 using strip and split:", device1)

# REMOVE BLANKS
device1 = device1_str.replace(" ", "").split(",")
print("device1 removed blanks using split:", device1)

# REMOVE BLANKS, CHANGE COMMA TO COLON
device1_str_colon = device1_str.replace(" ", "").replace(",", ":")
print("device1 removed blanks, comma to colon:", device1_str_colon)

# LOOP WITH STRIP AND SPLIT
device1 = list()
for item in device1_str.split(","):
    device1.append(item.strip())
print("device1 using strip for each item:", device1)

# IGNORING CASE
print("\n\nIGNORING CASE")
model = "CSR1000V"
if model == "csr1000v":
    print(f"matched: {model}")
else:
    print(f"didn't match: {model}")

model = "CSR1000V"
if model.lower() == "csr1000v":
    print(f"matched: {model}")
else:
    print(f"didn't match: {model}")

# FINDING SUBSTRING
print("\n\nFINDING SUBSTRING")
version = "Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.11.1a, RELEASE SOFTWARE (fc1)"
expected_version = "Version 16.11.1a"
index = version.find(expected_version)
if index >= 0:
    print(f"found version: {expected_version} at location {index} ")
else:
    print(f"not found: {expected_version}")

# SEPARATING STRING COMPONENTS
print("\n\nSEPARATING VERSION STRING COMPONENTS")
version_info = version.replace(" ", "").split(",")
for version_info_part in version_info:
    print(f"version part: {version_info_part}")
