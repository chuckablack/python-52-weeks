from random import choice
import string


def create_devices(num_devices=1, num_subnets=1):

    # CREATE LIST OF DEVICES
    created_devices = list()

    if num_devices > 254 or num_subnets > 254:
        print("Error: too many devices and/or subnets requested")
        return created_devices

    for subnet_index in range(1, num_subnets+1):

        for device_index in range(1, num_devices+1):

            # CREATE DEVICE DICTIONARY
            device = dict()

            # RANDOM DEVICE NAME
            device["name"] = (
                    choice(["r2", "r3", "r4", "r6", "r10"])
                    + choice(["L", "U"])
                    + choice(string.ascii_letters)
            )

            # RANDOM VENDOR FROM CHOICE OF CISCO, JUNIPER, ARISTA
            device["vendor"] = choice(["cisco", "juniper", "arista"])
            if device["vendor"] == "cisco":
                device["os"] = choice(["ios", "iosxe", "iosxr", "nexus"])
                if device["os"] == "ios":
                    device["version"] = choice(["15", "15E", "15SY", "12.2SE"])
                elif device["os"] == "iosxe":
                    device["version"] = choice(["16.9", "16.7", "16.5", "16.3"])
                elif device["os"] == "iosxr":
                    device["version"] = choice(["6.2", "6.0", "5.4", "5.1"])
                elif device["os"] == "nexus":
                    device["version"] = choice(["8.2", "8.0", "7.3", "7.1"])
            elif device["vendor"] == "juniper":
                device["os"] = "junos"
                device["version"] = choice(["12.3R12-S15", "15.1R7-S6", "18.4R2-S3", "15.1X53-D591"])
            elif device["vendor"] == "arista":
                device["os"] = "eos"
                device["version"] = choice(["4.24.1F", "4.23.2F", "4.22.1F", "4.21.3F"])

            device["ip"] = "10.0." + str(subnet_index) + "." + str(device_index)

            created_devices.append(device)

    return created_devices


def create_network(num_devices=1, num_subnets=1):

    # We'll re-use the create_devices function we created earlier,
    # then modify it to become an entire set of subnets, devices, and interfaces.

    devices = create_devices(num_devices, num_subnets)

    # Once again we are just going to consider the subnet to be the first three bytes
    # of the IP address, just to simplify things for teaching

    network = dict()
    network["subnets"] = dict()

    for device in devices:

        # There are many ways to get the subnet address from an IP address,
        # but for simplicity we are just going to replace the last byte with "0"
        subnet_address_bytes = device["ip"].split(".")
        subnet_address_bytes[3] = "0"
        subnet_address = ".".join(subnet_address_bytes)

        if subnet_address not in network["subnets"]:

            network["subnets"][subnet_address] = dict()
            network["subnets"][subnet_address]["devices"] = list()

        network["subnets"][subnet_address]["devices"].append(device)

        # Add interfaces to the device we just processed
        interfaces = list()
        for index in range(0, choice([2, 4, 8])):
            interface = {
                "name": "g/0/0/" + str(index),
                "speed": choice(["10", "100", "1000"])
            }
            interfaces.append(interface)

        device["interfaces"] = interfaces

    return network
