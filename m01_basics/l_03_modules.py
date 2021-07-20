from tabulate import tabulate
# from l_03_create_devices import create_devices
from util.create_utils import create_devices

# --- Main program --------------------------------------------
if __name__ == '__main__':

    devices = create_devices(num_subnets=5, num_devices=3, random_ip=True)
    print("\n", tabulate(devices, headers="keys"))
