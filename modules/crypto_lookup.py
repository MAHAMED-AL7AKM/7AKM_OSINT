import requests
from colorama import Fore, Style
from prettytable import PrettyTable

def search(address):
    print(Fore.YELLOW + f"[*] Looking up Bitcoin address: {address}" + Style.RESET_ALL)
    try:
        url = f"https://blockchain.info/rawaddr/{address}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            table = PrettyTable()
            table.field_names = ["Field", "Value"]
            table.add_row(["Address", address])
            table.add_row(["Total Received (BTC)", data.get("total_received", 0) / 1e8])
            table.add_row(["Total Sent (BTC)", data.get("total_sent", 0) / 1e8])
            table.add_row(["Final Balance (BTC)", data.get("final_balance", 0) / 1e8])
            table.add_row(["Number of Transactions", data.get("n_tx", 0)])
            print(table)
            return data
        else:
            print(Fore.RED + "[!] Address not found or invalid.")
            return None
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return None