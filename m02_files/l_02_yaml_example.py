from l_00_inventory import inventory
import yaml

with open("l_00_inventory.yaml", "w") as yaml_out:
    yaml_out.write(yaml.dump(inventory))

with open("l_00_inventory.yaml", "r") as yaml_in:
    yaml_inventory = yaml_in.read()

print("\nyaml pretty version:")
print(yaml.dump(yaml.safe_load(yaml_inventory), indent=4))

print("\n----- compare saved inventory with original --------------------")
saved_inventory = yaml.safe_load(yaml_inventory)
if saved_inventory == inventory:
    print("-- worked: saved inventory equals original")
else:
    print("-- failed: saved inventory different from original")
