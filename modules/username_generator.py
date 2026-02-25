import random
import string
import requests
import time
from colorama import Fore, Style

def check_telegram(username):
    url = f"https://t.me/{username}"
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        if response.status_code == 404:
            return True
        if "tgme_page" in response.text and "If you have Telegram" in response.text:
            return True
        return False
    except:
        return False

def check_instagram(username):
    url = f"https://instagram.com/{username}"
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        if response.status_code == 404:
            return True
        if "page not found" in response.text.lower():
            return True
        return False
    except:
        return False

def generate_username(length):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_to_telegram(bot_token, chat_id, message):
    if not bot_token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except:
        return False

def main():
    print(Fore.YELLOW + "[*] Username Generator (Telegram/Instagram) - بدون API" + Style.RESET_ALL)
    print(Fore.CYAN + "="*50)
    
    print("Choose platform:")
    print("1. Telegram only")
    print("2. Instagram only")
    print("3. Both")
    platform_choice = input(Fore.MAGENTA + "Enter choice (1/2/3): ").strip()
    if platform_choice not in ['1','2','3']:
        print(Fore.RED + "Invalid choice.")
        return
    
    print(Fore.CYAN + "\nChoose username length:")
    print("1. 3 characters (triple)")
    print("2. 4 characters (quad)")
    print("3. Custom range (e.g., 5-8)")
    length_choice = input(Fore.MAGENTA + "Enter choice (1/2/3): ").strip()
    
    if length_choice == '1':
        min_len = max_len = 3
    elif length_choice == '2':
        min_len = max_len = 4
    elif length_choice == '3':
        range_input = input("Enter min and max (e.g., 5-8): ").strip()
        try:
            min_len, max_len = map(int, range_input.split('-'))
        except:
            print(Fore.RED + "Invalid range. Using 5-5.")
            min_len = max_len = 5
    else:
        print(Fore.RED + "Invalid choice.")
        return
    
    try:
        count = int(input(Fore.MAGENTA + "\nHow many usernames to check? (default 20): ") or "20")
    except:
        count = 20
    
    bot_token = input(Fore.MAGENTA + "Enter Telegram bot token (leave blank to skip): ").strip()
    chat_id = input(Fore.MAGENTA + "Enter Telegram chat ID (leave blank to skip): ").strip()
    
    print(Fore.GREEN + f"\n[+] Generating and checking {count} usernames...")
    print(Fore.CYAN + "This may take a while (with 1s delay between checks).\n")
    
    available = []
    
    for i in range(count):
        length = random.randint(min_len, max_len)
        username = generate_username(length)
        
        status = ""
        tg_avail = ig_avail = False
        
        if platform_choice in ['1','3']:
            tg_avail = check_telegram(username)
            status += f"TG:{'✅' if tg_avail else '❌'}"
        if platform_choice in ['2','3']:
            ig_avail = check_instagram(username)
            status += f" IG:{'✅' if ig_avail else '❌'}"
        
        if (platform_choice == '1' and tg_avail) or \
           (platform_choice == '2' and ig_avail) or \
           (platform_choice == '3' and (tg_avail or ig_avail)):
            available.append((username, tg_avail, ig_avail))
        
        print(f"{i+1:2d}. {username:10s} {status}")
        time.sleep(1)
    
    if available:
        print(Fore.GREEN + f"\n[+] Found {len(available)} available username(s):")
        message = "<b>🎯 Available Usernames Found:</b>\n\n"
        for user, tg, ig in available:
            platforms = []
            if tg:
                platforms.append("Telegram")
            if ig:
                platforms.append("Instagram")
            platform_str = ', '.join(platforms)
            line = f"User: {user}\nPlatforms: {platform_str}\n-Tool 7AKM OSINT -\n- Developer : @G_X_V_7\n\n"
            print(Fore.CYAN + line)
            message += line
        
        if bot_token and chat_id:
            if send_to_telegram(bot_token, chat_id, message):
                print(Fore.GREEN + "[+] Results sent to Telegram.")
            else:
                print(Fore.RED + "[-] Failed to send to Telegram.")
    else:
        print(Fore.YELLOW + "\n[-] No available usernames found.")
        if bot_token and chat_id:
            send_to_telegram(bot_token, chat_id, "No available usernames found this time.")
    
    print(Fore.CYAN + "\nDone.")