from datetime import datetime, timedelta
import argparse
from time import sleep
import requests
import yaml
from ServiceMonitor import HttpMonitor, DnsMonitor, NtpMonitor, IcmpMonitor
from concurrent.futures import ThreadPoolExecutor

MONITOR_INTERVAL = 60
DISCOVERY_INTERVAL = 300

parser = argparse.ArgumentParser(description="Threadpool example")
parser.add_argument('-poolsize',  default=10, help='Size of the threadpool')
args = parser.parse_args()
threadpool_size = int(args.poolsize)


def get_services():

    print("\n\n----> Retrieving services ...", end="")
    response = requests.get("http://127.0.0.1:5001/services")
    if response.status_code != 200:
        print(f" !!!  Failed to retrieve services from server: {response.reason}")
        return {}

    print(" Services successfully retrieved")
    return response.json()


def discovery():

    # 'discovery' of services means reading them from the services.yaml file
    print(
        "\n\n----- Discovery services from inventory ---------------------"
    )
    with open("services.yaml", "r") as yaml_in:
        yaml_services = yaml_in.read()
        services = yaml.safe_load(yaml_services)

    existing_services = get_services()

    for service in services:

        if service["name"] in existing_services:
            continue

        if "data" not in service:
            service["data"] = ""
        service["availability"] = False
        service["response_time"] = 0.0
        service["last_heard"] = ""

        update_service(service)


def update_service(service):

    print(f"----> Updating service status via REST API: {service['name']}", end="")
    rsp = requests.put("http://127.0.0.1:5001/services", params={"name": service["name"]}, json=service)
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error posting to /services, response: {rsp.status_code}, {rsp.content}"
        )
        print(f" !!!  Unsuccessful attempt to update service status via REST API: {service['name']}")
    else:
        print(f" Successfully updated service status via REST API: {service['name']}")


def get_service_status(service):

    try:
        if service["type"].lower() == "http" or service["type"] == "https":
            monitor = HttpMonitor(service["name"], service["target"])
        elif service["type"].lower() == "dns":
            monitor = DnsMonitor(service["name"], service["target"], service["data"])
        elif service["type"].lower() == "ntp":
            monitor = NtpMonitor(service["name"], service["target"])
        elif service["type"].lower() == "icmp":
            monitor = IcmpMonitor(service["name"], service["target"])
        else:
            print(f" !!!  Unsupported service type: {service['type']}")
            return

        availability, response_time = monitor.get_status()

        service["availability"] = availability
        if service["availability"]:
            service["response_time"] = response_time
            service["last_heard"] = str(datetime.now())[:-3]

    except BaseException as e:
        print(f"  !!! Failed to get status for service {service['name']}: {e}")
        service["availability"] = False

    update_service(service)


def main():

    last_discovery = datetime.now()-timedelta(days=1)

    while True:

        if (datetime.now() - last_discovery).total_seconds() > DISCOVERY_INTERVAL:
            discovery()
            last_discovery = datetime.now()

        services = get_services()

        with ThreadPoolExecutor(max_workers=threadpool_size) as executor:
            executor.map(get_service_status, services.values())

        sleep(MONITOR_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting service-monitor")
        exit()
