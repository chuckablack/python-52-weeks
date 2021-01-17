from l_00_inventory import csv_inventory
import csv
from pprint import pprint

with open("l_00_inventory.csv", "w") as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerows(csv_inventory)

with open("l_00_inventory.csv", "r") as csv_in:
    csv_reader = csv.reader(csv_in)
    saved_csv_inventory = list()
    for device in csv_reader:
        saved_csv_inventory.append(device)

print("l_00_inventory.csv file:\n", saved_csv_inventory)

print("\ncsv pretty version:")
pprint(saved_csv_inventory)

print("\n----- compare saved inventory with original --------------------")
if saved_csv_inventory == csv_inventory:
    print("-- worked: saved inventory equals original")
else:
    print("-- failed: saved inventory different from original")
