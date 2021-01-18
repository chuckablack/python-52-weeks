from l_00_inventory import xml_inventory
import xmltodict
import json

# CONVERT PYTHON DATA TO XML AND WRITE TO FILE
with open("l_00_inventory.xml", "w") as xml_out:
    xml_out.write(xmltodict.unparse(xml_inventory, pretty=True))

# READ IN XML FROM FILE AND CONVERT TO PYTHON DATA
with open("l_00_inventory.xml", "r") as xml_in:
    saved_inventory = xmltodict.parse(xml_in.read())

print("\n----- xml pretty version --------------------")
print(xmltodict.unparse(saved_inventory, pretty=True))

# COMPARE ORIGINAL WITH CONVERTED AND SAVED DATA
print("\n----- compare saved inventory with original --------------------")
if saved_inventory == xml_inventory:
    print("-- worked: saved inventory equals original")
else:
    print("-- failed: saved inventory different from original")
