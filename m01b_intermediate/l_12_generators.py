from m01_basics.util.create_utils import create_device, create_devices, create_devices_gen
import time


# --- Main program --------------------------------------------
if __name__ == '__main__':

    devices = create_devices(num_devices=254, num_subnets=254)

    # Create dictionary pointing at those same devices
    devices_dict = dict()
    for device in devices:
        devices_dict[device["ip"]] = device

    devices_gen = create_devices_gen(num_devices=254, num_subnets=254)

    while True:

        ip_to_find = input("\nEnter IP address to find: ")
        if not ip_to_find:
            break

        start = time.time()
        for device in devices_gen:
            if device["ip"] == ip_to_find:
                print(f"---> found it (generator): {device}")
                generator_search_time = (time.time() - start) * 1000
                print(f"--- ---> in:  {generator_search_time} msec")
                print(f"--- ---> id of device:", id(device))
                break
        else:
            print(f"---! IP address not found, try again")
            continue

        start = time.time()
        if ip_to_find in devices_dict:
            print(f"---> found it (dict): {devices_dict[ip_to_find]}")
            dict_search_time = (time.time() - start) * 1000
            print(f"--- ---> in:  {dict_search_time} msec")
            print(f"--- ---> id of device:", id(devices_dict[ip_to_find]))

            print(f"conclusion: dictionary search was {int(generator_search_time/dict_search_time)}" +
                  f"times faster than generator search")

    # SIMPLE GENERATOR COMPREHENSION
    print("\n\n____ DEVICE INFO PARSING USING GENERATOR COMPREHENSION ____________________\n")
    device_str = "  r3-L-n7, cisco, catalyst 2960, ios , extra stupid stuff "
    device_gen = (item for item in device_str.split(","))
    device = [item.strip() for item in device_gen]
    print("device using generator comprehension:\n\t\t", device)

    # MORE INTERESTING GENERATOR COMPREHENSION
    print("\n\n____ DEVICE CREATION USING GENERATOR COMPREHENSION ____________________\n")
    devices_gen = (create_device(i, 1) for i in range(1, 25))
    for device in devices_gen:
        print(device)
