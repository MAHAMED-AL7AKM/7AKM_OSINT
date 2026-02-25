#!/usr/bin/env python3
import sys
import os
import subprocess
from colorama import Fore, Style, init
from utils.banner import show_banner
from modules import (
    username_lookup, ip_lookup, domain_lookup, phone_lookup,
    metadata_extract, url_analyzer, crypto_lookup, port_scan,
    fake_identity, username_generator, ai_chat
)

init(autoreset=True)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_menu():
    print(Fore.CYAN + "\n" + "="*60)
    print(Fore.YELLOW + "                7AKM OSINT 💀🔥 MAIN MENU")
    print(Fore.CYAN + "="*60)
    menu_options = [
        ("1", "👤 Username Search (Social Media)"),
        ("2", "📍 IP Geolocation & Reputation"),
        ("3", "🌐 Domain Analysis (DNS + Whois)"),
        ("4", "📱 Phone Number Lookup (Offline)"),
        ("5", "🖼️ Metadata Extraction (Images, PDFs, Audio)"),
        ("6", "🔗 URL Analyzer (Redirects, IP, Components)"),
        ("7", "₿ Bitcoin Address Lookup"),
        ("8", "🔌 Port Scanner (Open Ports)"),
        ("9", "🆔 Generate Fake Identity (with photo)"),
        ("10", "🎲 Generate Usernames (Telegram/Instagram) - بدون API"),
        ("11", "🤖 AI Chat with Identity (requires Gemini API key)"),
        ("12", "🔄 Update Tool (git pull)"),
        ("13", "ℹ️ Developer Info"),
        ("0", "❌ Exit")
    ]
    for num, desc in menu_options:
        print(Fore.GREEN + f"  {num}. {desc}")
    print(Fore.CYAN + "="*60)

def get_target_input(prompt_text):
    return input(Fore.MAGENTA + prompt_text + Style.RESET_ALL).strip()

def update_tool():
    print(Fore.YELLOW + "[*] Checking for updates..." + Style.RESET_ALL)
    try:
        # Run git pull
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode == 0:
            print(Fore.GREEN + "[+] Update successful!" + Style.RESET_ALL)
            print(result.stdout)
        else:
            print(Fore.RED + "[!] Update failed:" + Style.RESET_ALL)
            print(result.stderr)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)
    input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)

def developer_info():
    info = f"""
{Fore.CYAN}═══════════════════════════════════════════
{Fore.YELLOW}            DEVELOPER INFORMATION
{Fore.CYAN}═══════════════════════════════════════════

{Fore.GREEN}🔹 Tool Name    : {Fore.WHITE}7AKM OSINT 💀🔥
{Fore.GREEN}🔹 Version      : {Fore.WHITE}4.0
{Fore.GREEN}🔹 Developer    : {Fore.WHITE}MAHAMED-AL7AKM
{Fore.GREEN}🔹 Telegram     : {Fore.WHITE}@G_X_V_7
{Fore.GREEN}🔹 GitHub       : {Fore.WHITE}https://github.com/MAHAMED-AL7AKM/7AKM_OSINT
{Fore.GREEN}🔹 Description  : {Fore.WHITE}Ultimate OSINT tool for Termux
{Fore.GREEN}🔹 Modules      : {Fore.WHITE}11 OSINT tools + Fake Identity + AI Chat

{Fore.CYAN}═══════════════════════════════════════════
{Fore.YELLOW}        Thanks for using 7AKM OSINT! 💀🔥
{Fore.CYAN}═══════════════════════════════════════════
    """
    print(info)
    input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)

def main():
    while True:
        clear_screen()
        show_banner()
        print_menu()
        choice = input(Fore.YELLOW + "\n🔹 Choose option: " + Style.RESET_ALL).strip()

        if choice == "0":
            print(Fore.RED + "\n👋 Exiting... Goodbye!")
            sys.exit(0)

        target = None
        if choice in ["1","2","3","7","8"]:
            target = get_target_input("🔹 Enter target (username/IP/domain/address/...): ")
            if not target:
                print(Fore.RED + "❌ No input provided!")
                input(Fore.CYAN + "\nPress Enter to continue...")
                continue
        elif choice == "4":
            target = get_target_input("🔹 Enter phone number (with country code, e.g., +20123456789): ")
            if not target:
                print(Fore.RED + "❌ No input provided!")
                input(Fore.CYAN + "\nPress Enter to continue...")
                continue
        elif choice == "5":
            target = get_target_input("🔹 Enter file path (e.g., /sdcard/Download/image.jpg): ")
            if not os.path.exists(target):
                print(Fore.RED + "❌ File not found!")
                input(Fore.CYAN + "\nPress Enter to continue...")
                continue
        elif choice == "6":
            target = get_target_input("🔹 Enter URL (including http/https): ")
        elif choice == "9":
            # لا تحتاج هدف
            pass
        elif choice == "10":
            # لا تحتاج هدف
            pass
        elif choice == "11":
            target = get_target_input("🔹 Enter identity ID (folder name in identities/): ")
            if not target or not os.path.exists(f"identities/{target}"):
                print(Fore.RED + "❌ Identity not found! Generate one first (option 9).")
                input(Fore.CYAN + "\nPress Enter to continue...")
                continue
        elif choice == "12":
            update_tool()
            continue
        elif choice == "13":
            developer_info()
            continue
        else:
            print(Fore.RED + "❌ Invalid choice!")
            input(Fore.CYAN + "\nPress Enter to continue...")
            continue

        # تنفيذ الوحدة المختارة
        result = None
        try:
            if choice == "1":
                result = username_lookup.search(target)
            elif choice == "2":
                result = ip_lookup.search(target)
            elif choice == "3":
                result = domain_lookup.search(target)
            elif choice == "4":
                result = phone_lookup.search(target)
            elif choice == "5":
                result = metadata_extract.search(target)
            elif choice == "6":
                result = url_analyzer.search(target)
            elif choice == "7":
                result = crypto_lookup.search(target)
            elif choice == "8":
                result = port_scan.search(target)
            elif choice == "9":
                result = fake_identity.generate()
            elif choice == "10":
                username_generator.main()
                result = None
            elif choice == "11":
                ai_chat.start_chat(target)
                result = None
            else:
                print(Fore.RED + "❌ Not implemented yet!")
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}")

        if result and choice not in ["9","10","11"]:
            save_opt = input(Fore.YELLOW + "\n💾 Save output? (y/n): ").lower()
            if save_opt == 'y':
                from utils.helpers import timestamp
                import json
                filename = f"reports/{choice}_{timestamp()}.json"
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=4)
                print(Fore.GREEN + f"✅ Saved to {filename}")

        input(Fore.CYAN + "\nPress Enter to continue...")

if __name__ == "__main__":
    main()
