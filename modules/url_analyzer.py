import requests
from urllib.parse import urlparse
import socket
from colorama import Fore, Style
from prettytable import PrettyTable

def search(url):
    print(Fore.YELLOW + f"[*] Analyzing URL: {url}" + Style.RESET_ALL)
    result = {"url": url, "redirects": [], "final_url": url, "components": {}, "ip": None}

    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
        result["final_url"] = r.url
        if r.history:
            for resp in r.history:
                result["redirects"].append(resp.url)

        parsed = urlparse(r.url)
        result["components"] = {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": parsed.query,
            "fragment": parsed.fragment
        }
        ip = socket.gethostbyname(parsed.netloc)
        result["ip"] = ip

        table = PrettyTable()
        table.field_names = ["Field", "Value"]
        table.add_row(["Final URL", result["final_url"]])
        table.add_row(["IP", result["ip"]])
        for k, v in result["components"].items():
            table.add_row([k, v])
        if result["redirects"]:
            table.add_row(["Redirects", " -> ".join(result["redirects"])])
        print(table)
        return result
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return None