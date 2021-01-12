from util.create_utils import create_devices
from pprint import pprint

# --- Main program --------------------------------------------
if __name__ == '__main__':

    devices = tuple(create_devices(num_devices=4, num_subnets=1))

    print("\n----- LIST OF DEVICES --------------------")
    pprint(devices)
