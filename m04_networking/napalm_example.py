import napalm
import json


print("\n----- connecting to device (SSH) ----------")
driver = napalm.get_network_driver('ios')
with driver(hostname='ios-xe-mgmt.cisco.com',
            username='developer',
            password='C1sco12345',
            optional_args={'port': 8181}) as device:

    print("\n----- facts ----------")
    print(json.dumps(device.get_facts(), sort_keys=True, indent=4))

    print("\n----- interfaces ----------")
    print(json.dumps(device.get_interfaces(), sort_keys=True, indent=4))

    print("\n----- vlans ----------")
    print(json.dumps(device.get_vlans(), sort_keys=True, indent=4))

    print("\n----- snmp ----------")
    print(json.dumps(device.get_snmp_information(), sort_keys=True, indent=4))

    print("\n----- interface counters ----------")
    print(json.dumps(device.get_interfaces_counters(), sort_keys=True, indent=4))

    print("\n----- environment ----------")
    print(json.dumps(device.get_environment(), sort_keys=True, indent=4))


# print("\n----- connecting to device (NX-API) ----------")
# driver = napalm.get_network_driver('nxos')
# with driver(hostname='sbx-nxos-mgmt.cisco.com',
#             username='admin',
#             password='Admin_1234!',
#             # optional_args={'port': 10000}) as device:
#             ) as device:
#
#     print("\n----- facts ----------")
#     print(json.dumps(device.get_facts(), sort_keys=True, indent=4))
#
#     print("\n----- interfaces ----------")
#     print(json.dumps(device.get_interfaces(), sort_keys=True, indent=4))
#
#     print("\n----- vlans ----------")
#     print(json.dumps(device.get_vlans(), sort_keys=True, indent=4))
#
#     print("\n----- snmp ----------")
#     print(json.dumps(device.get_snmp_information(), sort_keys=True, indent=4))
#
#     print("\n----- environment ----------")
#     print(json.dumps(device.get_environment(), sort_keys=True, indent=4))
