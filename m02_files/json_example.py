from inventory import inventory
import json

with open("inventory.json", "w") as json_out:
    json_out.write(json.dumps(inventory))

with open("inventory.json", "r") as json_in:
    json_inventory = json_in.read()

print("inventory.json file:", json_inventory)

print("\njson pretty version:")
print(json.dumps(json.loads(json_inventory), indent=4))
