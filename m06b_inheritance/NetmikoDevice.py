from Device import Device
from netmiko import Netmiko

from util import get_version_from_show, get_uptime_from_show


class NetmikoDevice(Device):

    def connect(self):
        print(f"\n\n----- Connecting to {self.hostname}:{self.port}")
        self.connection = Netmiko(
            self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            device_type=self.device_type,
        )
        print(f"----- Connected! --------------------")
        return True

    def get_facts(self):
        show_hostname_output = self.connection.send_command("show hostname")
        show_version_output = self.connection.send_command("show version")
        show_serial_output = self.connection.send_command("show license host-id")
        show_uptime_output = self.connection.send_command("show system uptime")

        facts = dict()
        facts["os_version"] = get_version_from_show(show_version_output)
        facts["hostname"] = show_hostname_output.strip()
        facts["serial_number"] = show_serial_output.strip()[20:]  # Don't do this :-)
        facts["uptime"] = get_uptime_from_show(show_uptime_output)

        return facts

    def disconnect(self):
        self.connection.disconnect()
        print(f"----- Disconnected! --------------------")
        return True
