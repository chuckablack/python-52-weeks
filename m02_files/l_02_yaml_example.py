from l_00_inventory import inventory
import yaml

with open("l_00_inventory.yaml", "w") as yaml_out:
    yaml_out.write(yaml.dump(inventory))

with open("l_00_inventory.yaml", "r") as yaml_in:
    yaml_inventory = yaml_in.read()

print("l_00_inventory.yaml file:\n", yaml_inventory)

print("\nyaml pretty version:")
print(yaml.dump(yaml.safe_load(yaml_inventory), indent=4))
