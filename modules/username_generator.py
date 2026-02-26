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
        if response.status_code == 404:
            return True
        if "tgme_page" in response.text and "If you have Telegram" in response.text:
            return True
        return False
    except:
        return False

def check_instagram(username):
    """Check if Instagram username is available"""
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

def generate_username_double_dot():
    """Generate username like y__u."""
    letters = string.ascii_lowercase
    return f"{random.choice(letters)}__{random.choice(letters)}."

def generate_username_triple_dot():
    """Generate username like v_x__n."""
    letters = string.ascii_lowercase
    return f"{random.choice(letters)}_{random.choice(letters)}__{random.choice(letters)}."

def generate_username_random(length):
    """Generate random username of given length (letters+digits)"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_to_telegram(bot_token, chat_id, message):
    """Send message via Telegram bot"""
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
    print(Fore.YELLOW + "[*] Username Generator (Telegram/Instagram)" + Style.RESET_ALL)
    print(Fore.CYAN + "="*50)
    
    # Choose platform (only relevant if checking is enabled)
    print("Choose platform (for checking only):")
    print("1. Telegram only")
    print("2. Instagram only")
    print("3. Both")
    platform_choice = input(Fore.MAGENTA + "Enter choice (1/2/3): ").strip()
    if platform_choice not in ['1','2','3']:
        print(Fore.RED + "Invalid choice. Using Both.")
        platform_choice = '3'
    
    # Choose username pattern
    print(Fore.CYAN + "\nChoose username pattern:")
    print("1. Double-dot style (e.g., y__u.)")
    print("2. Triple-dot style (e.g., v_x__n.)")
    print("3. Random letters/numbers (e.g., xczxvcz)")
    print("4. Custom length (3-8 characters)")
    print("5. Generate only (send to Telegram without checking)")
    pattern_choice = input(Fore.MAGENTA + "Enter choice (1/2/3/4/5): ").strip()
    
    # Determine generation function
    if pattern_choice == '1':
        generate_func = generate_username_double_dot
        description = "double-dot"
    elif pattern_choice == '2':
        generate_func = generate_username_triple_dot
        description = "triple-dot"
    elif pattern_choice == '3':
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
    elif pattern_choice == '5':
        # No checking, just generate and send
        generate_only = True
        # Ask for pattern again (within this option)
        print(Fore.CYAN + "\nChoose pattern to generate:")
        print("1. Double-dot style (e.g., y__u.)")
        print("2. Triple-dot style (e.g., v_x__n.)")
        print("3. Random letters/numbers (e.g., xczxvcz)")
        print("4. Custom length (3-8 characters)")
        sub_choice = input(Fore.MAGENTA + "Enter choice (1/2/3/4): ").strip()
        if sub_choice == '1':
            generate_func = generate_username_double_dot
            description = "double-dot"
        elif sub_choice == '2':
            generate_func = generate_username_triple_dot
            description = "triple-dot"
        elif sub_choice == '3':
            generate_func = lambda: generate_username_random(random.randint(3, 8))
            description = "random length (3-8)"
        elif sub_choice == '4':
            try:
                custom_len = int(input("Enter exact length (3-8): ").strip())
                if custom_len < 3 or custom_len > 8:
                    custom_len = 5
            except:
                custom_len = 5
            generate_func = lambda: generate_username_random(custom_len)
            description = f"fixed length {custom_len}"
        else:
            print(Fore.RED + "Invalid choice. Using random.")
            generate_func = lambda: generate_username_random(random.randint(3, 8))
            description = "random length (3-8)"
    else:
        print(Fore.RED + "Invalid choice.")
        return
    
    # Number of usernames to generate
    try:
        count = int(input(Fore.MAGENTA + "\nHow many usernames to generate? (default 20): ") or "20")
    except:
        count = 20
    
    # Telegram bot settings
    bot_token = input(Fore.MAGENTA + "Enter Telegram bot token: ").strip()
    chat_id = input(Fore.MAGENTA + "Enter Telegram chat ID: ").strip()
    
    if not bot_token or not chat_id:
        print(Fore.RED + "❌ Bot token and chat ID are required for sending.")
        return
    
    print(Fore.GREEN + f"\n[+] Generating {count} usernames ({description} style)...")
    
    generated = []
    message_lines = []
    
    for i in range(count):
        username = generate_func()
        generated.append(username)
        
        # Format the line as requested
        line = f"User: {username}\n-Tool 7AKM OSINT -\n- Developer : @G_X_V_7"
        message_lines.append(line)
        
        print(f"{i+1:2d}. {username}")
        # No sleep needed when not checking
    
    # Prepare full message
    full_message = "<b>🎲 Generated Usernames:</b>\n\n" + "\n\n".join(message_lines)
    
    # Send to Telegram
    if send_to_telegram(bot_token, chat_id, full_message):
        print(Fore.GREEN + f"\n[+] Successfully sent {count} usernames to Telegram.")
    else:
        print(Fore.RED + "\n[-] Failed to send to Telegram.")
    
    print(Fore.CYAN + "\nDone.")

if __name__ == "__main__":
    main()
