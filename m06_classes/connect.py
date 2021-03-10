from netmiko import Netmiko
import napalm
from ncclient import manager

from misc_types import DeviceType

# NOTE: this will disable insecure HTTPS request warnings that NAPALM gets
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def connect_netmiko(hostname, username, password, port, device_type):

    print(f"\n\n----- Connecting to {hostname}:{port}")
    netmiko_connection = Netmiko(
        hostname,
        port=port,
        username=username,
        password=password,
        device_type=device_type,
    )
    print(f"----- Connected! --------------------")

    return netmiko_connection


def disconnect_netmiko(connection):
    connection.disconnect()
    print(f"----- Disconnected! --------------------")


def connect_napalm(hostname, username, password, port, device_type):

    driver = napalm.get_network_driver(device_type)
    if device_type == DeviceType.NXOS:
        napalm_device = driver(
            hostname=hostname,
            username=username,
            password=password,
        )
    elif device_type == DeviceType.IOS or device_type == DeviceType.NXOS_SSH:
        napalm_device = driver(
            hostname=hostname,
            username=username,
            password=password,
            optional_args={"port": port},
        )
    else:
        return None

    print(f"\n\n----- Connecting to {hostname}:{port}")
    napalm_device.open()
    print(f"----- Connected! --------------------")

    return napalm_device


def disconnect_napalm(connection):
    connection.close()
    print(f"----- Disconnected! --------------------")


def connect_ncclient(hostname, username, password, port, device_type):

    print(f"\n\n----- Connecting to {hostname}:{port}")
    nc_connection = manager.connect(
        host=hostname,
        port=port,
        username=username,
        password=password,
        device_params={"name": device_type},
        hostkey_verify=False,
    )
    print(f"----- Connected! --------------------")

    return nc_connection


def disconnect_ncclient(connection):
    connection.close_session()
    print(f"----- Disconnected! --------------------")
