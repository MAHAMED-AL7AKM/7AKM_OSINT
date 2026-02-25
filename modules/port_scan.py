import nmap
from colorama import Fore, Style
from prettytable import PrettyTable

def search(target):
    print(Fore.YELLOW + f"[*] Scanning ports for: {target}" + Style.RESET_ALL)
    nm = nmap.PortScanner()
    try:
        nm.scan(target, '1-1024', arguments='-T4')
        result = {}
        for host in nm.all_hosts():
            result[host] = {}
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                result[host][proto] = list(ports)
                print(Fore.GREEN + f"[+] Open ports on {host} ({proto}):" + Style.RESET_ALL)
                for port in ports:
                    print(f"    {port}: {nm[host][proto][port]['name']}")
        return result
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return None