import re
import subprocess
import optparse


def get_arument():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Inter to change its MAC address')
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC address')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] changing MAC address for" + interface + "to" + new_mac)
    subprocess.call(["ipconfig", interface, "down"], shell=True)
    subprocess.call(["ipconfig", interface, "hw", "ether", new_mac], shell=True)
    subprocess.call(["ipconfig", interface, "up"], shell=True)


if __name__ == '__main__':
    options = get_arument()
    change_mac(options.interface, options.new_mac)
    ifconfig_result = subprocess.check_output(['ifconfig', options.interface])
    print(ifconfig_result)

    mac_address_search_result = re.search(r"\w\w:" * 5 + r"\w\w", ifconfig_result)
    if mac_address_search_result:
        print(mac_address_search_result)
    else:
        print('Error')
