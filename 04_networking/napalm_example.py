import napalm
import json

driver = napalm.get_network_driver('ios')

print("\n----- connecting to device ----------")
device = driver(hostname='ios-xe-mgmt-latest.cisco.com',
                username='developer',
                password='C1sco12345',
                optional_args={'port': 8181})

device.open()
print("\n----- facts ----------")
print(json.dumps(device.get_facts(), sort_keys=True, indent=4))

print("\n----- interfaces ----------")
print(json.dumps(device.get_interfaces(), sort_keys=True, indent=4))

print("\n----- vlans ----------")
print(json.dumps(device.get_vlans(), sort_keys=True, indent=4))

print("\n----- snmp ----------")
print(json.dumps(device.get_snmp_information(), sort_keys=True, indent=4))
