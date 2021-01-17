from l_00_inventory import inventory
import json

with open("l_00_inventory.json", "w") as json_out:
    json_out.write(json.dumps(inventory))

with open("l_00_inventory.json", "r") as json_in:
    json_inventory = json_in.read()

print("l_00_inventory.json file:", json_inventory)

print("\njson pretty version:")
print(json.dumps(json.loads(json_inventory), indent=4))

print("\n----- compare saved inventory with original --------------------")
saved_inventory = json.loads(json_inventory)
if saved_inventory == inventory:
    print("-- worked: saved inventory equals original")
else:
    print("-- failed: saved inventory different from original")
