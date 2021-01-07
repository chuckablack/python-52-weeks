from util.create_utils import create_devices
from tabulate import tabulate
from operator import itemgetter
from pprint import pprint

# --- Main program --------------------------------------------
if __name__ == '__main__':

    t = (1, 2, 3)
    t += (4, 5)
    print(t)

    devices = create_devices(num_devices=4, num_subnets=1)
    devices_tuple = tuple(devices)

    print("\n----- LIST OF DEVICES --------------------")
    pprint(devices)

    print("\n----- TUPLE OF DEVICES --------------------")
    pprint(devices_tuple)

