from datetime import datetime, timedelta
from time import sleep
import requests
import napalm
from napalm.base.exceptions import NapalmException
import yaml
import socket
import time
import re

MONITOR_INTERVAL = 15
DISCOVERY_INTERVAL = 300


def get_version(device, facts):

    if device["os"] == "iosxe":

        re_version_pattern = r"Version (.*),"
        version_match = re.search(re_version_pattern, facts["os_version"])
        if version_match:
            return version_match.group(1)
        else:
            return "--"

    return facts["os_version"]


def get_devices():

    print("\n\n----> Retrieving devices ...", end="")
    response = requests.get("http://127.0.0.1:5001/devices")
    if response.status_code != 200:
        print(f" !!!  Failed to retrieve devices from server: {response.reason}")
        return {}

    print(" Devices successfully retrieved")
    return response.json()


def discovery():

    # 'discovery' of devices means reading them from the devices.yaml file
    print(
        "\n\n----- Discovery devices from inventory ---------------------"
    )
    with open("devices.yaml", "r") as yaml_in:
        yaml_devices = yaml_in.read()
        devices = yaml.safe_load(yaml_devices)

    existing_devices = get_devices()

    for device in devices:

        try:
            device["ip_address"] = socket.gethostbyname(device["hostname"])
        except (socket.error, socket.gaierror) as e:
            print(f"  !!! Error attempting to get ip address for device {device['hostname']}: {e}")
            device["ip_address"] = ""

        if device["name"] in existing_devices:
            existing_devices[device["name"]]["ip_address"] = device["ip_address"]
            device = existing_devices[device["name"]]

        else:
            device["availability"] = False
            device["response_time"] = 0.0
            device["model"] = ""
            device["os_version"] = ""
            device["last_heard"] = ""

        update_device(device)


def update_device(device):

    print(f"----> Updating device status via REST API: {device['name']}", end="")
    rsp = requests.put("http://127.0.0.1:5001/devices", params={"name": device["name"]}, json=device)
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error posting to /devices, response: {rsp.status_code}, {rsp.content}"
        )
        print(f" !!!  Unsuccessful attempt to update device status via REST API: {device['name']}")
    else:
        print(f" Successfully updated device status via REST API: {device['name']}")


def get_device_facts(device):

    try:
        if device["os"] == "ios" or device["os"] == "iosxe":
            driver = napalm.get_network_driver("ios")
        elif device["os"] == "nxos-ssh":
            driver = napalm.get_network_driver("nxos_ssh")
        elif device["os"] == "nxos":
            driver = napalm.get_network_driver("nxos")
        else:
            driver = napalm.get_network_driver(device["os"])  # try this, it will probably fail

        napalm_device = driver(
            hostname=device["hostname"],
            username=device["username"],
            password=device["password"],
            optional_args={"port": device["ssh_port"]},
        )
        napalm_device.open()

        time_start = time.time()
        facts = napalm_device.get_facts()
        response_time = time.time() - time_start

        device["os_version"] = get_version(device, facts)
        device["model"] = facts["model"]
        device["availability"] = True
        device["response_time"] = response_time
        device["last_heard"] = str(datetime.now())[:-3]

    except BaseException as e:
        print(f"  !!! Failed to get facts for device {device['name']}: {e}")
        device["availability"] = False


def main():

    last_discovery = datetime.now()-timedelta(days=1)

    while True:

        if (datetime.now() - last_discovery).total_seconds() > DISCOVERY_INTERVAL:
            discovery()
            last_discovery = datetime.now()

        devices = get_devices()
        for device in devices.values():
            get_device_facts(device)
            update_device(device)

        sleep(MONITOR_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting device-monitor")
        exit()
