import napalm
import json

driver = napalm.get_network_driver('ios')

device = driver(hostname='ios-xe-mgmt-latest.cisco.com',
                username='developer',
                password='C1sco12345',
                optional_args={'port': 8181})

device.open()
print(json.dumps(device.get_interfaces(), sort_keys=True, indent=4))