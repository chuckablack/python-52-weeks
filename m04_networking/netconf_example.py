from ncclient import manager
from lxml import etree

# the following comment/lines are to workaround a PyCharm bug
# noinspection PyUnresolvedReferences
from xml.dom.minidom import parseString

csr_device_1 = {
    "host": "ios-xe-mgmt.cisco.com",
    "port": 10000,
    "username": "developer",
    "password": "C1sco12345",
    "device_params": {"name": "csr"},
}
csr_device_2 = {
    "host": "ios-xe-mgmt-latest.cisco.com",
    "port": 10000,
    "username": "developer",
    "password": "C1sco12345",
    "device_params": {"name": "csr"},
}
nxos_device = {
    "host": "sbx-nxos-mgmt.cisco.com",
    "port": 10000,
    "username": "admin",
    "password": "Admin_1234!",
    "device_params": {"name": "nexus"},
}

for device in [csr_device_1, csr_device_2]:

    print(f"\n----- Retrieving XML configuration from: {device['host']} --------------------")
    nc_connection = manager.connect(
        host=device["host"],
        port=device["port"],
        username=device["username"],
        password=device["password"],
        device_params=device["device_params"],
        hostkey_verify=False,
    )

    config = nc_connection.get_config("running")
    print(f"\n----- XML get_config() output from: {device['host']}")
    print(str(etree.tostring(config.data_ele, pretty_print=True).decode()))

    # 'get()' doesn't seem to work on these devices
    # get_all = nc_connection.get()
    # print(f"\n----- XML get() output from: {device['host']}")
    # print(str(etree.tostring(get_all.data_ele, pretty_print=True).decode()))

    xml_doc = parseString(str(config))
    version = xml_doc.getElementsByTagName("version")
    print(f"\n----- Device OS version, hostname, email from: {device['host']}")
    if len(version) > 0:
        print(f"        version: {version[0].firstChild.nodeValue}")
    else:
        print(f"        Unable to retrieve version!")

    hostname = xml_doc.getElementsByTagName("hostname")
    if len(hostname) > 0:
        print(f"        hostname: {hostname[0].firstChild.nodeValue}")
    else:
        print(f"        Unable to retrieve hostname!")

    email = xml_doc.getElementsByTagName("contact-email-addr")
    if len(email) > 0:
        print(f"        email: {email[0].firstChild.nodeValue}")
    else:
        print(f"        Unable to retrieve email!")

    usernames = xml_doc.getElementsByTagName("username")
    for username in usernames:
        name = username.getElementsByTagName("name")
        if len(name) > 0:
            print(f"        name: {name[0].firstChild.nodeValue}")
        else:
            print(f"        Unable to retrieve name from username!")
