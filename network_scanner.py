import scapy.all as sc
# sc.ls(sc.ARP()) узнает какие переменые передаються


def scan(ip):
    arp_request = sc.ARP(pdst=ip)
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = sc.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    print("\tIP\t\tMAC Address\n----------------------------------------------------------------------------")
    for element in answered_list:
        print(element[1].psrc + "\t\t" + element[1].hwsrc)


scan('192.168.100.1/24')
