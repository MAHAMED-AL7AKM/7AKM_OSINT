import random
import string
import requests
import time
from colorama import Fore, Style

def check_telegram(username):
    """Check if Telegram username is available"""
    url = f"https://t.me/{username}"
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        # If user doesn't exist, Telegram returns 404
        if response.status_code == 404:
            return True
        # Sometimes returns 302 (redirect) if exists, but better check content
        if "tgme_page" in response.text and "If you have Telegram" in response.text:
            return True  # Not found
        return False
    except:
        return False

def check_instagram(username):
    """Check if Instagram username is available"""
    url = f"https://instagram.com/{username}"
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        # Instagram returns 404 if account doesn't exist
        if response.status_code == 404:
            return True
        # Sometimes returns 200 with "Page Not Found" text
        if "page not found" in response.text.lower():
            return True
        return False
    except:
        return False

def generate_username_double_dot():
    """Generate username like y__u. (double dot style)"""
    # Pattern: letter + '__' + letter + '.'
    letters = string.ascii_lowercase
    return f"{random.choice(letters)}__{random.choice(letters)}."

def generate_username_triple_dot():
    """Generate username like v_x__n. (triple dot style)"""
    # Pattern: letter + '_' + letter + '__' + letter + '.'
    letters = string.ascii_lowercase
    return f"{random.choice(letters)}_{random.choice(letters)}__{random.choice(letters)}."

def generate_username_random(length):
    """Generate random username of given length (letters+digits)"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_to_telegram(bot_token, chat_id, message):
    """Send message via Telegram bot (optional)"""
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
    print(Fore.YELLOW + "[*] Username Generator (Telegram/Instagram) - No API required" + Style.RESET_ALL)
    print(Fore.CYAN + "="*50)
    
    # Choose platform
    print("Choose platform:")
    print("1. Telegram only")
    print("2. Instagram only")
    print("3. Both")
    platform_choice = input(Fore.MAGENTA + "Enter choice (1/2/3): ").strip()
    if platform_choice not in ['1','2','3']:
        print(Fore.RED + "Invalid choice.")
        return
    
    # Choose username pattern
    print(Fore.CYAN + "\nChoose username pattern:")
    print("1. Double-dot style (e.g., y__u.)")
    print("2. Triple-dot style (e.g., v_x__n.)")
    print("3. Random letters/numbers (e.g., xczxvcz)")
    print("4. Custom length (3-8 characters)")
    pattern_choice = input(Fore.MAGENTA + "Enter choice (1/2/3/4): ").strip()
    
    # Determine how to generate usernames based on pattern
    if pattern_choice == '1':
        generate_func = generate_username_double_dot
        description = "double-dot"
    elif pattern_choice == '2':
        generate_func = generate_username_triple_dot
        description = "triple-dot"
    elif pattern_choice == '3':
        # Random with variable length (3-8)
        generate_func = lambda: generate_username_random(random.randint(3, 8))
        description = "random length (3-8)"
    elif pattern_choice == '4':
        try:
            custom_len = int(input("Enter exact length (3-8): ").strip())
            if custom_len < 3 or custom_len > 8:
                print(Fore.RED + "Length must be between 3 and 8. Using 5.")
                custom_len = 5
        except:
            print(Fore.RED + "Invalid input. Using length 5.")
            custom_len = 5
        generate_func = lambda: generate_username_random(custom_len)
        description = f"fixed length {custom_len}"
    else:
        print(Fore.RED + "Invalid choice.")
        return
    
    # Number of usernames to check
    try:
        count = int(input(Fore.MAGENTA + "\nHow many usernames to generate? (default 20): ") or "20")
    except:
        count = 20
    
    # Telegram bot settings (optional)
    bot_token = input(Fore.MAGENTA + "Enter Telegram bot token (leave blank to skip): ").strip()
    chat_id = input(Fore.MAGENTA + "Enter Telegram chat ID (leave blank to skip): ").strip()
    
    print(Fore.GREEN + f"\n[+] Generating and checking {count} usernames ({description} style)...")
    print(Fore.CYAN + "This may take a while (with 1s delay between checks).\n")
    
    available = []
    
    for i in range(count):
        username = generate_func()
        
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
        
        print(f"{i+1:2d}. {username:15s} {status}")
        time.sleep(1)  # Avoid rate limiting
    
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

if __name__ == "__main__":
    main()
