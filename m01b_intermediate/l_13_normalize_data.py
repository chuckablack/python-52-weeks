from ipaddress import IPv4Address

# REMOVE CAPITALIZATION ISSUES
device_1 = {
    "name": "sbx-n9kv-ao",
    "vendor": "cisco",
    "model": "Nexus9000 C9300v Chassis",
    "os": "nxos",
    "version": "9.3(3)",
    "ip": "10.1.1.1",
    1: "any data goes here",
}
device_2 = {
    "name": "SBX-n9kv-AO",
    "vendor": "Cisco",
    "model": "Nexus9000 C9300v Chassis",
    "os": "NXOS",
    "version": "9.3(3)",
    "ip": "10.1.1.1",
    1: "any data goes here",
}
if (
    device_1["name"].lower() == device_2["name"].lower()
    and device_1["vendor"].lower() == device_2["vendor"].lower()
    and device_1["model"].lower() == device_2["model"].lower()
    and device_1["os"].lower() == device_2["os"].lower()
):
    print("--\nString lower() normalization works")
else:
    print("--\nString lower() normalization failed")

# MAC ADDRESS NORMALIZATION

mac_addr_colons = "a0:b1:c2:d3:e4:f5"
mac_addr_caps = "A0:B1:C2:D3:E4:F5"
mac_addr_dots = "a0b1.c2d3.e4f5"
mac_addr_hyphens = "A0-B1-C2-D3-E4-F5"
mac_addr_wacky = "A0-b1.C2:D3.e4-f5"

mac_addr_norm = "a0b1c2d3e4f5"


# Return normalized MAC addresses
def normalize(mac):
    return mac.lower().replace(":", "").replace(".", "").replace("-", "")


# print("MAC address with colons:  ", normalize(mac_addr_colons))
# print("MAC address with caps:    ", normalize(mac_addr_caps))
# print("MAC address with dots:    ", normalize(mac_addr_dots))
# print("MAC address with hyphens: ", normalize(mac_addr_hyphens))
# print("MAC address with wacky:   ", normalize(mac_addr_wacky))

if (
    normalize(mac_addr_colons)
    == normalize(mac_addr_caps)
    == normalize(mac_addr_dots)
    == normalize(mac_addr_hyphens)
    == normalize(mac_addr_wacky)
    == mac_addr_norm
):
    print("--\nMAC address normalization works")
else:
    print("--\nMAC address normalization failed")

# IP ADDRESS NORMALIZATION

ip_addr_1 = "10.0.1.1"
ip_addr_2 = "10.000.001.001"

if IPv4Address(ip_addr_1) == IPv4Address(ip_addr_2):
    print("--\nIP address normalization works")
else:
    print("--\nIP address normalization failed")
