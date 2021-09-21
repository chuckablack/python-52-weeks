import copy

import napalm
# NOTE: this will disable insecure HTTPS request warnings that NAPALM gets
import urllib3

from connect import cisco_sandbox_devices

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


IOS = "ios"
NXOS = "nxos"
NXOS_SSH = "nxos_ssh"

devices = copy.deepcopy(cisco_sandbox_devices)

# make a copy of NXOS, so we can do both SSH and NXAPI connections
devices[NXOS_SSH] = copy.deepcopy(devices[NXOS])

for device_type, device in devices.items():

    print(f"\n\n----- connecting to device {device_type}: {device['hostname']} ----------")
    driver = napalm.get_network_driver(device_type)
    if device_type == NXOS:
        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
        )
        continue  # seems to be a bug in NAPALM for this device type
    else:
        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
            optional_args={"port": device["port"]},
        )

    print(f"----- connect to                device {device['hostname']}, type: {device_type} ----------")
    napalm_device.open()

    print(f"----- get configuration for     device {device['hostname']}, type: {device_type} ----------")
    # Note: we have to special-case NXOS, which require a checkpoint file for doing comparison
    if device_type == NXOS or device_type == NXOS_SSH:
        config_for_compare = napalm_device._get_checkpoint_file()
    else:
        config_for_compare = napalm_device.get_config()["running"]

    with open(f"cisco.{device_type}.config", "w") as config_out:
        config_out.write(config_for_compare)

    print(f"----- load candidate config for device {device['hostname']}, type: {device_type} ----------")
    napalm_device.load_replace_candidate(filename=f"cisco.{device_type}.config")
    print(f"----- compare config for        device {device['hostname']}, type: {device_type} ----------")
    diff = napalm_device.compare_config()
    print(f"----- diff output for           device {device['hostname']}, type: {device_type} ----------")
    print(f"diff:\n{diff}")

    napalm_device.close()
