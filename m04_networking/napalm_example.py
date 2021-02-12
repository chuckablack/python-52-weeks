import napalm
import json
import copy
from connect import cisco_sandbox_devices

# NOTE: this will disable insecure HTTPS request warnings that NAPALM gets
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


IOS = "ios"
NXOS = "nxos"
NXOS_SSH = "nxos_ssh"

devices = copy.deepcopy(cisco_sandbox_devices)

# make a copy of NXOS, so we can do both SSH and NXAPI connections
devices[NXOS_SSH] = copy.deepcopy(devices[NXOS])

for device_type, device in devices.items():

    print(f"\n----- connecting to device {device_type}: {device['hostname']} ----------")
    driver = napalm.get_network_driver(device_type)
    if device_type == NXOS:
        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
        )
    else:
        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
            optional_args={"port": device["port"]},
        )

    napalm_device.open()

    print("\n----- facts ----------")
    print(json.dumps(napalm_device.get_facts(), sort_keys=True, indent=4))

    print("\n----- interfaces ----------")
    print(json.dumps(napalm_device.get_interfaces(), sort_keys=True, indent=4))

    print("\n----- vlans ----------")
    print(json.dumps(napalm_device.get_vlans(), sort_keys=True, indent=4))

    print("\n----- snmp ----------")
    print(
        json.dumps(napalm_device.get_snmp_information(), sort_keys=True, indent=4)
    )

    print("\n----- interface counters ----------")
    try:
        print(
            json.dumps(
                napalm_device.get_interfaces_counters(), sort_keys=True, indent=4
            )
        )
    except NotImplementedError as e:
        print(f"oops, looks like this isn't implemented for {device['hostname']}, error: {e}")

    print("\n----- environment ----------")
    try:
        print(json.dumps(napalm_device.get_environment(), sort_keys=True, indent=4))
    except (KeyError, IOError) as e:
        print(f"oops, looks like there is a NAPALM exception for {device['hostname']}, error: {e}")

    napalm_device.close()
