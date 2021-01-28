from ncclient import manager
from lxml import etree
import xmltodict
from pprint import pprint


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

# for device in [nxos_device]:
for device in [csr_device_1]:

    print(f"\n----- Retrieving XML configuration from: {device['host']} --------------------")
    nc_connection = manager.connect(
        host=device["host"],
        port=device["port"],
        username=device["username"],
        password=device["password"],
        device_params=device["device_params"],
        hostkey_verify=False,
    )

    if device["device_params"]["name"] == "nexus":

        serial_number_xml_nxos = '<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><serial/></System>'
        version_xml_nxos = '<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device"><version/></System>'

        rsp = nc_connection.get(('subtree', serial_number_xml_nxos))
        print(f"\n----- XML get() serial number subtree from: {device['host']}")
        print(str(etree.tostring(rsp.data_ele, pretty_print=True).decode()))

        vlans_filter = '''
                        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
                            <vlan>
                            </vlan>
                        </System>
                       '''
        rsp = nc_connection.get(('subtree', vlans_filter))
        print(f"\n----- XML get() vlans subtree from: {device['host']}")
        print(str(etree.tostring(rsp.data_ele, pretty_print=True).decode()))

        rsp = nc_connection.get(('subtree', version_xml_nxos))
        print(f"\n----- XML get() version subtree from: {device['host']}")
        print(str(etree.tostring(rsp.data_ele, pretty_print=True).decode()))

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

    version = xml_doc.getElementsByTagName("version")
    print(f"\n----- Device OS version, hostname, email from: {device['host']}")
    if len(version) > 0:
        print(f"        version: {version[0].firstChild.nodeValue}")
    else:
        print(f"        Unable to retrieve version!")

    version_xml_get = """
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <version></version>
    </native>
    """
    rsp = nc_connection.get(("subtree", version_xml_get))
    print(f"\n----- XML get() version subtree from: {device['host']}")
    print(str(etree.tostring(rsp.data_ele, pretty_print=True).decode()))

    config = nc_connection.get_config("running")
    print(f"\n----- XML get() output from: {device['host']}")
    print(str(etree.tostring(config.data_ele, pretty_print=True).decode()))

    # Cisco-IOS-XE-process-cpu-oper.yang
    netconf_filter = '''
                      <filter>
                        <cpu-usage xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-process-cpu-oper">
                        </cpu-usage>
                      </filter>
                    '''

    rsp = nc_connection.get(netconf_filter)
    print(f"\n----- XML get() cpu subtree from: {device['host']}")
    print(str(etree.tostring(rsp.data_ele, pretty_print=True).decode()))

    # Cisco-IOS-XE-memory-oper.yang
    netconf_filter = '''
                      <filter>
                        <memory-statistics xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper">
                        </memory-statistics>
                      </filter>
                    '''

    rsp = nc_connection.get(netconf_filter)
    print(f"\n----- XML get() memory subtree from: {device['host']}")
    print(str(etree.tostring(rsp.data_ele, pretty_print=True).decode()))

    memory_statistics = xmltodict.parse(str(etree.tostring(rsp.data_ele, pretty_print=True).decode()), dict_constructor=dict)
    print("\n----- Memory statistics --------------------\n")
    pprint(memory_statistics)
