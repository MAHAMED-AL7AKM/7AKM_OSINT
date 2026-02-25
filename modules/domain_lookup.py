import dns.resolver
import whois
from colorama import Fore, Style
from prettytable import PrettyTable

def search(domain):
    print(Fore.YELLOW + f"[*] Analyzing domain: {domain}" + Style.RESET_ALL)
    result = {"domain": domain, "dns": {}, "whois": {}}

    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            result["dns"][rtype] = [str(r) for r in answers]
        except:
            result["dns"][rtype] = []

    try:
        w = whois.whois(domain)
        result["whois"]["registrar"] = w.registrar
        result["whois"]["creation_date"] = str(w.creation_date)
        result["whois"]["expiration_date"] = str(w.expiration_date)
        result["whois"]["name_servers"] = w.name_servers
    except Exception as e:
        result["whois"]["error"] = str(e)

    for rtype, records in result["dns"].items():
        if records:
            print(Fore.GREEN + f"[+] {rtype} records:" + Style.RESET_ALL)
            for rec in records:
                print(f"    {rec}")

    print(Fore.GREEN + "[+] Whois Info:" + Style.RESET_ALL)
    for k, v in result["whois"].items():
        if v:
            print(f"    {k}: {v}")

    return result