from inventory import inventory
import yaml

with open("inventory.yaml", "w") as yaml_out:
    yaml_out.write(yaml.dump(inventory))

with open("inventory.yaml", "r") as yaml_in:
    yaml_inventory = yaml_in.read()

print("inventory.yaml file:\n", yaml_inventory)

print("\nyaml pretty version:")
print(yaml.dump(yaml.load(yaml_inventory), indent=4))
