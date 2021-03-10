from Device import Device
import napalm

from misc_types import DeviceType

# NOTE: this will disable insecure HTTPS request warnings that NAPALM gets
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NapalmDevice(Device):

    def connect(self):
        driver = napalm.get_network_driver(self.device_type)
        if self.device_type == DeviceType.NXOS:
            self.connection = driver(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
            )
        elif self.device_type == DeviceType.IOS or self.device_type == DeviceType.NXOS_SSH:
            self.connection = driver(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                optional_args={"port": self.port},
            )
        else:
            return False

        print(f"\n\n----- Connecting to {self.hostname}:{self.port}")
        self.connection.open()
        print(f"----- Connected! --------------------")

        return True

    def get_facts(self):
        return self.connection.get_facts()

    def disconnect(self):
        self.connection.close()
        print(f"----- Disconnected! --------------------")
        return True
