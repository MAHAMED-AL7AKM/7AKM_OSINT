import requests
from colorama import Fore, Style
from prettytable import PrettyTable

def search(ip):
    print(Fore.YELLOW + f"[*] Looking up IP: {ip}" + Style.RESET_ALL)
    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,org,as,mobile,proxy,hosting,query"
    try:
        r = requests.get(url)
        data = r.json()
        if data.get("status") == "success":
            table = PrettyTable()
            table.field_names = ["Field", "Value"]
            for key, value in data.items():
                if key != "status":
                    table.add_row([key, value])
            print(table)
            return {"module": "ip", "target": ip, "data": data}
        else:
            print(Fore.RED + f"[!] Error: {data.get('message')}")
            return None
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return None