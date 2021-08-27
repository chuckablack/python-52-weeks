from connect import netmiko_connect
import re

SHOW_IP_ROUTE = "ip route"
SHOW_ARP = "arp"
SHOW_INT_DESCRIPTION = "int description"
SHOW_INT_BRIEF = "int brief"
SHOW_VERSION = "version"

IOS = "ios"
NXOS = "nxos"
IOSXR = "iosxr"
commands = {SHOW_IP_ROUTE: {IOS: "show ip route",
                            NXOS: "show ip route",
                            IOSXR: "show ip route"},
            SHOW_ARP: {IOS: "show arp",
                       NXOS: "show ip arp",
                       IOSXR: "show arp"},
            SHOW_INT_DESCRIPTION: {IOS: "show interfaces description",
                                   NXOS: "show interface description",
                                   IOSXR: "show interfaces description"},
            SHOW_INT_BRIEF: {IOS: "show ip interface brief",
                             NXOS: "show interface brief",
                             IOSXR: "show ip interface brief"},
            SHOW_VERSION: {IOS: "show version",
                           NXOS: "show version",
                           IOSXR: "show version"}
            }

# CYCLE THROUGH DIFFERENT DEVICE TYPES
for device_type in [IOSXR]:

    connection = netmiko_connect(device_type)
    print('connection:', connection)

    print(f"\n\n----- showing running configuration for {device_type} -------------------")
    output = connection.send_command("show running-config")
    print(output)

    print(f"\n\n----- showing ip route for {device_type} -------------------")
    output = connection.send_command(commands[SHOW_IP_ROUTE][device_type])
    print(output)

    print(f"\n\n----- showing arp table for {device_type} -------------------")
    output = connection.send_command(commands[SHOW_ARP][device_type])
    print(output)

    print(f"\n\n----- showing interface description for {device_type} -------------------")
    output = connection.send_command(commands[SHOW_INT_DESCRIPTION][device_type])
    print(output)

    print(f"\n\n----- showing interface brief for {device_type} -------------------")
    output = connection.send_command(commands[SHOW_INT_BRIEF][device_type])
    print(output)

    connection.disconnect()

# CYCLE THROUGH DIFFERENT SHOW COMMANDS
print("\n\nBEGIN CYCLE THROUGH DIFFERENT SHOW COMMANDS")
# csr_connection = netmiko_connect(IOS)
# nxos_connection = netmiko_connect(NXOS)
xr_connection = netmiko_connect(IOSXR)


if xr_connection:
    print("--- connections successful")
else:
    exit()

nxos_version_raw = None
csr_version_raw = None
xr_version_raw = None

for command_type, command in commands.items():

    print(f"\n----- command: {command_type} ---------------------")

    # print(f"\n----- ... for IOS: {command[IOS]} ---------------------")
    # csr_output = csr_connection.send_command(command[IOS])
    # print(csr_output)
    #
    # print(f"\n----- ... for NXOS: {command[NXOS]} ---------------------")
    # nxos_output = nxos_connection.send_command(command[NXOS])
    # print(nxos_output)

    print(f"\n----- ... for IOSXR: {command[IOSXR]} ---------------------")
    xr_output = xr_connection.send_command(command[IOSXR])
    print(xr_output)

    # saving versions for later parsing
    if command_type == SHOW_VERSION:
        # csr_version_raw = csr_output
        # nxos_version_raw = nxos_output
        xr_version_raw = xr_output

# csr_connection.disconnect()
# nxos_connection.disconnect()
xr_connection.disconnect()

# Now the harder part - parsing the output into some 'normalized' format
# if nxos_version_raw and csr_version_raw:
if xr_version_raw:

    # re_nxos_version_pattern = r"NXOS: version (.*)"
    # re_csr_version_pattern = r"Cisco IOS XE Software, Version (.*)"
    re_xr_version_pattern = r"Cisco IOS XR Software, Version (.*)"

    # nxos_version_match = re.search(re_nxos_version_pattern, nxos_version_raw)
    # csr_version_match = re.search(re_csr_version_pattern, csr_version_raw)
    xr_version_match = re.search(re_xr_version_pattern, xr_version_raw)

    # if nxos_version_match:
    #     print(f"---> NXOS version parsed from output: {nxos_version_match.group(1)}")
    #
    # if csr_version_match:
    #     print(f"---> IOS version parsed from output:  {csr_version_match.group(1)}")

    if xr_version_match:
        print(f"---> IOSXR version parsed from output:  {xr_version_match.group(1)}")

else:
    print(f"!!! error, no version data to parse")
