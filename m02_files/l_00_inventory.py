inventory = [
    {
        "name": "devnet-csr-always-on-sandbox",
        "ssh-info": {
            "hostname": "ios-xe-mgmt-latest.cisco.com",
            "port": 8181,
            "credentials": {"username": "developer", "password": "C1sco12345"},
            "device_type": "cisco_ios",
        },
        "netconf-info": {"port": 10000},
        "restconf-info": {"port": 9443},
    },
    {
        "name": "devnet-csr-always-on-sandbox",
        "ssh-info": {
            "hostname": "sbx-nxos-mgmt.cisco.com",
            "port": 8181,
            "credentials": {"username": "admin", "password": "Admin_1234!"},
            "device_type": "cisco_nxos",
        },
    },
]

csv_inventory = [
    [
        "devnet-csr-always-on-sandbox",
        "ios-xe-mgmt-latest.cisco.com",
        "8181",
        "developer",
        "C1sco12345",
    ],
    [
        "devnet-csr-always-on-sandbox",
        "sbx-nxos-mgmt.cisco.com",
        "8181",
        "admin",
        "Admin_1234!",
    ],
]

xml_inventory = {
    "inventory": {
        "devices": [
            {
                "name": "devnet-csr-always-on-sandbox",
                "ssh-info": {
                    "hostname": "ios-xe-mgmt-latest.cisco.com",
                    "port": "8181",
                    "credentials": {"username": "developer", "password": "C1sco12345"},
                    "device_type": "cisco_ios",
                },
                "netconf-info": {"port": "10000"},
                "restconf-info": {"port": "9443"},
            },
            {
                "name": "devnet-csr-always-on-sandbox",
                "ssh-info": {
                    "hostname": "sbx-nxos-mgmt.cisco.com",
                    "port": "8181",
                    "credentials": {"username": "admin", "password": "Admin_1234!"},
                    "device_type": "cisco_nxos",
                },
            },
        ]
    }
}


def get_inventory():
    return inventory
