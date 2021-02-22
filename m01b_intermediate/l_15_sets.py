available_ips = set()
used_ips = set()


def print_ips():

    print(f"Available IPs: {available_ips}")
    print(f"Used IPs:      {used_ips}")


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
