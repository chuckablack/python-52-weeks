from connect import connect

SHOW_IP_ROUTE = "show ip route"
SHOW_ARP = "show arp"
SHOW_INT_DESCRIPTION = "show int description"
SHOW_INT_BRIEF = "show int brief"

CSR = "csr"
NXOS = "nxos"
commands = {SHOW_IP_ROUTE: {CSR: "show ip route",
                            NXOS: "show ip route"},
            SHOW_ARP: {CSR: "show arp",
                       NXOS: "show ip arp"},
            SHOW_INT_DESCRIPTION: {CSR: "show int description",
                                   NXOS: "show int description"},
            SHOW_INT_BRIEF: {CSR: "show interface brief",
                             NXOS: "show interface brief"}
            }

for device_type in [CSR, NXOS]:
    connection = connect(device_type)
    # print('connection:', connection)
    # output = connection.send_command("show running-config")
    # print(output)

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
