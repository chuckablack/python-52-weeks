from Device import Device
from ncclient import manager
import xmltodict


class NcclientDevice(Device):

    def connect(self):
        print(f"\n\n----- Connecting to {self.hostname}:{self.port}")
        self.connection = manager.connect(
            host=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            device_params={"name": self.device_type},
            hostkey_verify=False,
        )
        print(f"----- Connected! --------------------")

        return True

    def get_facts(self):
        facts = dict()

        serial_number_xml_nxos = '<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><serial/></System>'
        rsp = self.connection.get(("subtree", serial_number_xml_nxos))
        serial_xml = xmltodict.parse(rsp.data_xml, dict_constructor=dict)

        facts["serial_number"] = serial_xml["data"]["System"]["serial"]

        return facts

    def disconnect(self):
        self.connection.close_session()
        print(f"----- Disconnected! --------------------")
        return True
