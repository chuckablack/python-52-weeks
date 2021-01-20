available_ips = set()
used_ips = set()


def print_ips():

    print(f"Available IPs: {available_ips}")
    print(f"Used IPs:      {used_ips}")

    # available_ips_list = list(available_ips)
    # used_ips_list = list(used_ips)
    #
    # if len(available_ips_list) > len(used_ips_list):
    #     for _ in range(0, len(available_ips_list) - len(used_ips_list)):
    #         used_ips_list.append("")
    # elif len(available_ips_list) < len(used_ips_list):
    #     for _ in range(0, len(used_ips_list) - len(available_ips_list)):
    #         available_ips_list.append("")
    #
    # print()
    # print("          available   used")
    # print("   ----------------   -----------------")
    # for available_ip, used_ip in zip(available_ips_list, used_ips_list):
    #     print(f"   {available_ip:>16}   {used_ip:<16}")


for index in range(180, 200, 3):
    available_ips.add("10.0.1." + str(index))

print_ips()
while True:
    ip_address = input("\nEnter IP address to allocate: ")
    if not ip_address:
        print("\nExiting 'sets' application")
        exit()

    if ip_address in available_ips:

        print(f"-- allocated IP address: {ip_address}")
        available_ips.remove(ip_address)
        used_ips.add(ip_address)

        print_ips()

        if len(available_ips.intersection(used_ips)) > 0:
            print("\n-- ERROR! one or more IPs in both sets")

    else:
        print("-- IP address not found in available IPs\n")
