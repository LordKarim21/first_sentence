import scapy.all as sc
import argparse


# sc.ls() узнает какие переменые передаються


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP / IP range')
    options = parser.parse_args()
    return options


def scan(ip):
    arp_request = sc.ARP(pdst=ip)
    broadcast = sc.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = sc.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_info(clients_list):
    print("\tIP\t\t\tMAC Address\n----------------------------------------------------------------------------")
    for client in clients_list:
        print(client['ip'] + "\t\t", client['mac'])


option = get_argument()
if option.target:
    scan_result = scan(option.target)
else:
    scan_result = scan('192.168.100.1/24')
print_info(scan_result)
