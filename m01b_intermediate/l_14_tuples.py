from m01_basics.util.create_utils import create_devices
from pprint import pprint
from collections import namedtuple

# --- Main program --------------------------------------------
if __name__ == '__main__':

    # devices_list = create_devices(num_devices=4, num_subnets=1)
    # devices_tuple = tuple(devices_list)
    #
    # print("\n----- LIST OF DEVICES --------------------")
    # pprint(devices_list)
    # print("\n----- TUPLE OF DEVICES --------------------")
    # pprint(devices_tuple)
    #
    # print("\n----- DEVICE AS TUPLE --------------------")
    # device = ("sbx-n9kv-ao", "cisco", "Nexus9000 C9300v Chassis", "nxos", "10.0.1.1")
    #
    # print("  name:", device[0])
    # print("vendor:", device[1])
    # print(" model:", device[2])
    # print("    os:", device[3])
    # print("    ip:", device[4])
    #
    # print("\n----- DEVICE AS TUPLE, FORMATTED WITH FOR LOOP -------------------")
    # item = ("name", "vendor", "model", "os", "ip")
    # for i in range(0, len(device)):
    #     print(f"{item[i]:>10s} : {device[i]}")
    #
    # print("\n----- DEVICE AS TUPLE, FOR LOOP ITERATING TUPLE -------------------")
    # item = ("name", "vendor", "model", "os", "ip")
    # for i, device_item in enumerate(device):
    #     print(f"{item[i]:>10s} : {device_item}")

    print("\n----- DEVICE AS NAMED TUPLE --------------------")
    Device = namedtuple('Device', ['name', 'vendor', 'model', 'os', 'ip'])
    device = Device("sbx-n9kv-ao", "cisco", "Nexus9000 C9300v Chassis", "nxos", "10.0.1.1")

    print("  name:", device.name)
    print("vendor:", device.vendor)
    print(" model:", device.model)
    print("    os:", device.os)
    print("    ip:", device.ip)

    print("\n----- PPRINT OF DEVICE NAMED TUPLE --------------------")
    pprint(device)

    print("\n----- CONVERT DEVICES TO NAMED TUPLES --------------------")
    devices = create_devices(num_devices=10, num_subnets=2, random_ip=True)
    devices_as_namedtuples = list()
    for device in devices:
        # Device = namedtuple("Device", device.keys())
        Device = namedtuple("Device", ["name", "vendor", "os", "version", "ip"])
        devices_as_namedtuples.append(Device(**device))

    print("\n----- PPRINT VERSION OF DEVICES AS NAMED TUPLES --------------------")
    pprint(devices_as_namedtuples)

    print("\n----- NICELY FORMATTED --------------------\n")
    print("   NAME      VENDOR : OS      IP ADDRESS")
    print("  -----     -------   -----   --------------")
    for device in devices_as_namedtuples:
        print(f'{device.name:>7}  {device.vendor:>10} : {device.os:<6}  {device.ip:<15}')
