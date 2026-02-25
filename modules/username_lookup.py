import requests
from colorama import Fore, Style
from prettytable import PrettyTable

def search(username):
    print(Fore.YELLOW + f"[*] Searching username: {username}" + Style.RESET_ALL)
    sites = [
        "twitter.com", "github.com", "instagram.com", "reddit.com",
        "tiktok.com", "youtube.com", "facebook.com", "pinterest.com",
        "snapchat.com", "telegram.org", "discord.com", "twitch.tv"
    ]
    table = PrettyTable()
    table.field_names = ["Site", "Profile URL"]
    found = 0
    for site in sites:
        url = f"https://{site}/{username}"
        try:
            r = requests.head(url, allow_redirects=True, timeout=5)
            if r.status_code == 200:
                table.add_row([site, url])
                found += 1
        except:
            pass
    if found > 0:
        print(table)
    else:
        print(Fore.CYAN + "[-] No profiles found.")
    return {"module": "username", "target": username, "found": found}