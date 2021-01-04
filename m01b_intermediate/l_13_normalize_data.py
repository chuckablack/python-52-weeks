mac_addr_colons = "a0:b1:c2:d3:e4:f5"
mac_addr_caps = "A0:B1:C2:D3:E4:F5"
mac_addr_dots = "a0b1.c2d3.e4f5"
mac_addr_hyphens = "A0-B1-C2-D3-E4-F5"
mac_addr_wacky = "A0-b1.C2:D3.e4-f5"

mac_addr_norm = "a0b1c2d3e4f5"

# Lower case

if mac_addr_colons == mac_addr_caps.lower():
    print("Correct - Equals")

else:
    print("Oops - no equals!")


print("--")

# Normalize
mac_addr_colons = mac_addr_colons.lower()
mac_addr_colons = mac_addr_colons.replace(":", "")
mac_addr_colons = mac_addr_colons.replace(".", "")
mac_addr_colons = mac_addr_colons.replace("-", "")

mac_addr_caps = mac_addr_caps.lower()
mac_addr_caps = mac_addr_caps.replace(":", "")
mac_addr_caps = mac_addr_caps.replace(".", "")
mac_addr_caps = mac_addr_caps.replace("-", "")

mac_addr_dots = mac_addr_dots.lower()
mac_addr_dots = mac_addr_dots.replace(":", "")
mac_addr_dots = mac_addr_dots.replace(".", "")
mac_addr_dots = mac_addr_dots.replace("-", "")

mac_addr_hyphens = mac_addr_hyphens.lower()
mac_addr_hyphens = mac_addr_hyphens.replace(":", "")
mac_addr_hyphens = mac_addr_hyphens.replace(".", "")
mac_addr_hyphens = mac_addr_hyphens.replace("-", "")

mac_addr_wacky = mac_addr_wacky.lower()
mac_addr_wacky = mac_addr_wacky.replace(":", "")
mac_addr_wacky = mac_addr_wacky.replace(".", "")
mac_addr_wacky = mac_addr_wacky.replace("-", "")

print("MAC address with colons:  ", mac_addr_colons)
print("MAC address with caps:    ", mac_addr_caps)
print("MAC address with dots:    ", mac_addr_dots)
print("MAC address with hyphens: ", mac_addr_hyphens)
print("MAC address with wacky:   ", mac_addr_wacky)

if (
    mac_addr_colons
    == mac_addr_caps
    == mac_addr_dots
    == mac_addr_hyphens
    == mac_addr_wacky
    == mac_addr_norm
):
    print("-- hooray it worked, all MAC addrs are equal")

else:
    print("--oops chuck you screwed up!")


print("--")

# Same thing but using a function for simplicity

mac_addr_colons = "a0:b1:c2:d3:e4:f5"
mac_addr_caps = "A0:B1:C2:D3:E4:F5"
mac_addr_dots = "a0b1.c2d3.e4f5"
mac_addr_hyphens = "A0-B1-C2-D3-E4-F5"
mac_addr_wacky = "A0-b1.C2:D3.e4-f5"


# Return normalized MAC addresses
def normalize(mac):
    return mac.lower().replace(":", "").replace(".", "").replace("-", "")


print("MAC address with colons:  ", normalize(mac_addr_colons))
print("MAC address with caps:    ", normalize(mac_addr_caps))
print("MAC address with dots:    ", normalize(mac_addr_dots))
print("MAC address with hyphens: ", normalize(mac_addr_hyphens))
print("MAC address with wacky:   ", normalize(mac_addr_wacky))

print("--")

if (
    normalize(mac_addr_colons)
    == normalize(mac_addr_caps)
    == normalize(mac_addr_dots)
    == normalize(mac_addr_hyphens)
    == normalize(mac_addr_wacky)
    == mac_addr_norm
):
    print("--hooray it works using functions!")
