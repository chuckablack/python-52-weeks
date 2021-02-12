import napalm
import filecmp
import difflib
import sys


print("\n----- connecting to device, comparing configs ----------")
print("\n----- connecting to device ----------")
driver = napalm.get_network_driver('ios')
with driver(hostname='ios-xe-mgmt.cisco.com',
            username='developer',
            password='C1sco12345',
            optional_args={'port': 8181}) as device:

    print("\n----- load_replace_candidate ----------")
    config = device.get_config()
    config_running = config["running"]

    # with open("cisco.iosxe.standard.config", "r") as config_out:
    #     config_standard = config_out.read()
    with open("cisco.iosxe.running.config", "w") as config_out:
        config_out.write(config["running"])

    # cmp = filecmp.cmp("cisco.iosxe.standard.config", "cisco.iosxe.running.config", shallow=False)
    # difflines = difflib.context_diff(config_running.splitlines(), config_standard.splitlines(), fromfile="running", tofile="standard")
    # for line in difflines:
    #     print(line)

    device.load_replace_candidate(filename="cisco.iosxe.running.config")
    diff = device.compare_config()
    print(diff)

print("\n----- connecting to device ----------")
# driver = napalm.get_network_driver('nxos_ssh')
driver = napalm.get_network_driver('nxos')
with driver(hostname='sbx-nxos-mgmt.cisco.com',
            username='admin',
            password='Admin_1234!',
            # optional_args={'port': 8181}) as device:
            ) as device:

    print("\n----- load_replace_candidate ----------")
    config = device.get_config()
    config_running = config["running"]

    with open("cisco.nxos.standard.config", "r") as config_out:
        config_standard = config_out.read()
    with open("cisco.nxos.running.config", "w") as config_out:
        config_out.write(config["running"])

    # cmp = filecmp.cmp("cisco.nxos.standard.config", "cisco.nxos.running.config", shallow=False)
    # difflines = difflib.context_diff(config_running.splitlines(), config_standard.splitlines(), fromfile="running", tofile="standard")
    # for line in difflines:
    #     print(line)

    device.load_replace_candidate(filename="cisco.nxos.running.config")
    diff = device.compare_config()
    print(diff)

