import re
from random import choice

re_mac_address = r"^([0-9A-Fa-f]{2}[:-]?){5}([0-9A-Fa-f]{2})$"
re_ip_address = (
    r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
    + r"([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
)
re_hostname = (
    r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*"
    + r"([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
)
re_email = (
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    + r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)


def rude_remark():
    return choice(["No way, Jose", "Give me a break, Jake", "Nice try, McFly"])


MAC_ADDRESS = "mac address"
IP_ADDRESS = "ip address"
HOSTNAME = "hostname"
EMAIL = "email"
validation_list = [MAC_ADDRESS, IP_ADDRESS, HOSTNAME, EMAIL]
validation_pattern = {MAC_ADDRESS: re_mac_address,
                      IP_ADDRESS: re_ip_address,
                      HOSTNAME: re_hostname,
                      EMAIL: re_email}

for validation_type in validation_list:

    print(f"\n----- {validation_type} verification --------------------")
    while True:

        input_to_validate = input(f"Enter {validation_type} or <cr> to quit:  ")
        if not input_to_validate:
            break

        match = re.search(validation_pattern[validation_type], input_to_validate.strip())
        if match is not None:
            print(f"---> valid {validation_type}: {match.group(0)} at index {match.start()}")
        else:
            print(f"---> {input_to_validate}?! ", end="")
            print(rude_remark())
