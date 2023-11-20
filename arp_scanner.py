"""

ARP Scanner

"""

from scapy.all import *

# We define subnet
ip_range = "192.168.1."

for i in range(1, 256):
    # We create a packet to be sent to broadcast ff:ff:ff:ff:ff:ff
    arp_packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_range + str(i), hwdst="ff:ff:ff:ff:ff:ff")

    # We use conf.L3socket to send layer 3 packets
    response_packet = srp1(arp_packet, timeout=1, verbose=0)

    if response_packet:
        print(f"IP: {response_packet[ARP].psrc} | MAC: {response_packet[ARP].hwsrc}")
