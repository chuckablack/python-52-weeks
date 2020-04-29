device_str = "  r3-L-n7, cisco, catalyst 2960, ios , extra stupid stuff "
device_info = [
    ("name", "r3-L-n7"),
    ("vendor", "cisco"),
    ("model", "catalyst 2960"),
    ("os", "ios"),
]

# LIST COMPREHENSION
device = [item.strip() for item in device_str.split(",")]
print("device using list comprehension:\n\t\t", device)

# LIST COMPREHENSION WITH CONDITIONAL
device = [item.strip() for item in device_str.split(",") if "stupid" not in item]
print("device using list comprehension with conditional:\n\t\t", device)

# DICT COMPREHENSION
device = {item[0]: item[1] for item in device_info}
print("device using dict comprehension:\n\t\t", device)
print("device nicely formatted:")
for key, value in device.items():
    print(f"{key:>16s} : {value}")
