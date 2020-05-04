from netmiko import Netmiko
from connect import connect


for device_type in ["csr", "nexus"]:

    connection = connect(device_type)
    print('connection:', connection)
    output = connection.send_command("show running-config")
    print(output)
