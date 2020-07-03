from l_03_functions import create_devices

devices = create_devices(25)

print()
print("        NAME      VENDOR  OS      IP ADDRESS")
print("       -----     -------  -----   -----------")
for device in devices:
    print(f'    {device["name"]:>8}  {device["vendor"]:>10}  {device["os"]:<6}  {device["ip"]:<15}')
