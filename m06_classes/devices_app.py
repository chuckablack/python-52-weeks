from Device import Device
from misc_types import DeviceType, TransportType
from pprint import pprint


def create_devices():
    created_devices = dict()
    created_devices["nxos-netmiko"] = Device(
        name="nxos-netmiko",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.CISCO_NXOS,
        transport=TransportType.NETMIKO,
    )
    created_devices["nxos-netmiko"].set_port(8181)
    created_devices["nxos-netmiko"].set_credentials(username="admin", password="Admin_1234!")

    created_devices["nxos-napalm"] = Device(
        name="nxos-napalm",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.NXOS,
        transport=TransportType.NAPALM,
    )
    created_devices["nxos-napalm"].set_port(8181)
    created_devices["nxos-napalm"].set_credentials(username="admin", password="Admin_1234!")

    created_devices["nxos-ncclient"] = Device(
        name="nxos-ncclient",
        hostname="sbx-nxos-mgmt.cisco.com",
        device_type=DeviceType.NEXUS,
        transport=TransportType.NCCLIENT,
    )
    created_devices["nxos-ncclient"].set_port(10000)
    created_devices["nxos-ncclient"].set_credentials(username="admin", password="Admin_1234!")

    return created_devices


devices = create_devices()
for _, device in devices.items():

    if not device.connect():
        print(f"----- Connection failed: {device.name}")
        continue

    facts = device.get_facts()
    print(f"----- Facts for device: {device.name}")
    pprint(facts)

    device.disconnect()
