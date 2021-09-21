from netmiko import Netmiko

cisco_sandbox_devices = {
    # "ios": {
    #     "hostname": "sandbox-iosxe-recomm-1.cisco.com",
    #     "port": 22,
    #     "username": "developer",
    #     "password": "C1sco12345",
    #     "device_type": "cisco_ios",
    # },
    # "iosxr": {
    #     "hostname": "sandbox-iosxr-1.cisco.com",
    #     "port": 22,
    #     "username": "admin",
    #     "password": "C1sco12345",
    #     "device_type": "cisco_ios",
    # },
    "nxos": {
        "hostname": "sandbox-nxos-1.cisco.com",
        "port": 22,
        "username": "admin",
        "password": "Admin_1234!",
        "device_type": "cisco_nxos",
    },
}


def netmiko_connect(device_type):

    print(
        f"\n\nConnecting to {cisco_sandbox_devices[device_type]['hostname']}:{cisco_sandbox_devices[device_type]['port']}"
    )
    print("... this may take a little while.")

    connection = Netmiko(
        cisco_sandbox_devices[device_type]["hostname"],
        port=cisco_sandbox_devices[device_type]["port"],
        username=cisco_sandbox_devices[device_type]["username"],
        password=cisco_sandbox_devices[device_type]["password"],
        device_type=cisco_sandbox_devices[device_type]["device_type"],
    )

    return connection


def disconnect(connection):
    connection.disconnect()
