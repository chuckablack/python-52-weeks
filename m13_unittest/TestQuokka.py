import inspect
import unittest
from datetime import datetime
import requests
import yaml
import io
from contextlib import redirect_stdout

from quokka_server.device_monitor import discovery as device_discovery
from quokka_server.service_monitor import discovery as service_discovery

# Note: these tests require the quokka server to be running,
#       with TESTDB database, e.g. with the following command:
#       export FLASK_APP=quokka_server.py ; export TESTDB ; flask run --port 5001

test_hosts = {
    "test-host-1": {
        "ip_address": "10.0.0.1",
        "mac_address": "00:11:22:33:44:01",
        "hostname": "test-host-1",
        "last_heard": str(datetime.now())[:-3],
        "availability": True,
        "response_time": "0.501",
    },
    "test-host-2": {
        "ip_address": "10.0.0.2",
        "mac_address": "00:11:22:33:44:02",
        "hostname": "test-host-2",
        "last_heard": str(datetime.now())[:-3],
        "availability": True,
        "response_time": "0.502",
    },
}


class TestQuokka(unittest.TestCase):

    def test_hosts(self):

        print(f"\n\n===== {self.__class__.__name__}: {inspect.stack()[0][3]} =================================\n")
        print("Storing hosts into quokka:")
        for hostname, host in test_hosts.items():
            rsp = requests.put("http://127.0.0.1:5001/hosts", params={"hostname": hostname}, json=host)
            self.assertEqual(rsp.status_code, 204, f"status code: expected 204, received {rsp.status_code}")
            print(f"---> host: {hostname} stored into quokka: success")

        print("\nRetrieving hosts from quokka:")
        rsp = requests.get("http://127.0.0.1:5001/hosts")
        self.assertEqual(rsp.status_code, 200, f"status code: expected 200, received {rsp.status_code}")
        hosts = rsp.json()
        print(f"---> Retrieved {len(hosts)} hosts: success")

        print(f"\nComparing hosts to originals")
        self.assertTrue(isinstance(hosts, dict))
        self.assertEqual(len(hosts), len(test_hosts), "wrong number of hosts retrieved")
        for hostname, host in hosts.items():
            self.assertTrue(hostname in test_hosts, f"hostname: {hostname} not in test_hosts")
            self.assertEqual(host, test_hosts[hostname], f"host not equal to test_host")
            print(f"---> Compared host: {hostname}: success")

    def test_devices(self):

        print(f"\n\n===== {self.__class__.__name__}: {inspect.stack()[0][3]} =================================\n")
        print("Discovering devices using device_monitor")
        with io.StringIO() as buf, redirect_stdout(buf):
            device_discovery()
        print("Discovering devices using device_monitor: completed")

        with open("devices.yaml", "r") as yaml_in:
            yaml_devices = yaml_in.read()
            devices_from_file = yaml.safe_load(yaml_devices)

        print("\nRetrieving devices from quokka:")
        rsp = requests.get("http://127.0.0.1:5001/devices")
        self.assertEqual(rsp.status_code, 200, f"status code: expected 200, received {rsp.status_code}")
        devices = rsp.json()
        print(f"---> Retrieved {len(devices)} devices: success")

        print(f"\nComparing hosts to originals")
        self.assertTrue(isinstance(devices, dict))
        self.assertEqual(len(devices), len(devices_from_file), "wrong number of devices retrieved")
        for device_from_file in devices_from_file:
            self.assertTrue(device_from_file["name"] in devices, f"device: {device_from_file['name']} not found in devices")
            device = devices[device_from_file["name"]]
            self.assertEqual(device_from_file["name"], device["name"], "device names do not match")
            self.assertEqual(device_from_file["os"], device["os"], "device oses do not match")
            self.assertEqual(device_from_file["hostname"], device["hostname"], "device hostnames do not match")
            self.assertEqual(device_from_file["password"], device["password"], "device passwords do not match")
            self.assertEqual(device_from_file["username"], device["username"], "device usernames do not match")
            self.assertEqual(device_from_file["vendor"], device["vendor"], "device vendors do not match")
            self.assertEqual(device_from_file["transport"], device["transport"], "device transports do not match")
            print(f"---> Compared device: {device['name']}: success")

    def test_services(self):

        print(f"\n\n===== {self.__class__.__name__}: {inspect.stack()[0][3]} =================================\n")
        print("Discovering services using service_monitor")
        with io.StringIO() as buf, redirect_stdout(buf):
            service_discovery()
        print("Discovering services using service_monitor: completed")

        with open("services.yaml", "r") as yaml_in:
            yaml_services = yaml_in.read()
            services_from_file = yaml.safe_load(yaml_services)

        print("\nRetrieving services from quokka:")
        rsp = requests.get("http://127.0.0.1:5001/services")
        self.assertEqual(rsp.status_code, 200, f"status code: expected 200, received {rsp.status_code}")
        services = rsp.json()
        print(f"---> Retrieved {len(services)} services: success")

        print(f"\nComparing services to originals")
        self.assertTrue(isinstance(services, dict))
        self.assertEqual(len(services), len(services_from_file), "wrong number of services retrieved")
        for service_from_file in services_from_file:
            self.assertTrue(service_from_file["name"] in services, f"service: {service_from_file['name']} not found in services")
            service = services[service_from_file["name"]]
            self.assertEqual(service_from_file["name"], service["name"], "service names do not match")
            self.assertEqual(service_from_file["type"], service["type"], "service types do not match")
            self.assertEqual(service_from_file["target"], service["target"], "service targets do not match")
            if "data" in service_from_file:
                self.assertEqual(service_from_file["data"], service["data"], "service passwords do not match")
            print(f"---> Compared service: {service['name']}: success")


if __name__ == "__main__":
    unittest.main()
