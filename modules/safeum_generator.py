import websocket
import ssl
import os
import json
import gzip
import requests
import random
import concurrent.futures
import threading
import sys
from time import sleep
from colorama import Fore, Style, init

# تهيئة colorama
init(autoreset=True)

# متغيرات عامة للإحصائيات
created = 0
failed = 0
running = True

# حروف عشوائية لإنشاء اسم المستخدم
ch = 'qwertyuioplkjhgfdsazxcvbnm'

# توقيع الأداة
TOOL_SIGNATURE = "-Tool 7AKM OSINT - - Developer : @G_X_V_7"

def generate_username():
    """توليد اسم مستخدم عشوائي"""
    return str(random.choice(ch)) + ''.join(random.choice(ch) for _ in range(9))

def create_account(bot_token, chat_id):
    """إنشاء حساب واحد وإرسال النتيجة إلى تليجرام"""
    global created, failed
    
    username = generate_username()
    
    # رسالة التليجرام مع التوقيع
    telegram_message = f""" افـرح يـسـطـا اكـونت  اهـوه 😂🫆

Username: {username}
Password: hhhh

{TOOL_SIGNATURE}"""
    
    headers = {
        "app": "com.safeum.android",
        "host": None,
        "remoteIp": "193.200.173.45",
        "remotePort": "8080",
        "sessionId": "b6cbb22d-06ca-41ff-8fda-c0ddeb148195",
        "time": "2023-04-30 12:13:32",
        "url": "wss://51.79.208.190/Auth"
    }
    
    data0 = {
        "action": "Register",
        "subaction": "Desktop",
        "locale": "en_GB",
        "gmt": "+02",
        "password": {
            "m1x": "503c73d12b354f86ff9706b2114704380876f59f1444133e62ca27b5ee8127cc",
            "m1y": "6387ae32b7087257452ae27fc8a925ddd6ba31d955639838249c02b3de175dfc",
            "m2": "219d1d9b049550f26a6c7b7914a44da1b5c931eff8692dbfe3127eeb1a922fcf",
            "iv": "e38cb9e83aef6ceb60a7a71493317903",
            "message": "0d99759f972c527722a18a74b3e0b3c6060fe1be3ad53581a7692ff67b7bb651a18cde40552972d6d0b1482e119abde6203f5ab4985940da19bb998bb73f523806ed67cc6c9dbd310fd59fedee420f32"
        },
        "magicword": {
            "m1x": "04eb364e4ef79f31f3e95df2a956e9c72ddc7b8ed4bf965f4cea42739dbe8a4a",
            "m1y": "ef1608faa151cb7989b0ba7f57b39822d7b282511a77c4d7a33afe8165bdc1ab",
            "m2": "4b4d1468bfaf01a82c574ea71c44052d3ecb7c2866a2ced102d0a1a55901c94b",
            "iv": "b31d0165dde6b3d204263d6ea4b96789",
            "message": "8c6ec7ce0b9108d882bb076be6e49fe2"
        },
        "magicwordhint": "0000",
        "login": username,
        "devicename": "Xiaomi Redmi Note 8 Pro",
        "softwareversion": "1.1.0.1380",
        "nickname": "hvtctchnjvfxfx",
        "os": "AND",
        "deviceuid": "c72d110c1ae40d50",
        "devicepushuid": "*dxT6B6Solm0:APA91bHqL8wxzlyKHckKxMDz66HmUqmxCPAVKBDrs8KcxCAjwdpxIPTCfRmeEw8Jks_q13vOSFsOVjCVhb-CkkKmTUsaiS7YOYHQS_pbH1g6P4N-jlnRzySQwGvqMP1gxRVksHiOXKKP",
        "osversion": "and_11.0.0",
        "id": "1734805704"
    }
    
    try:
        ws = websocket.create_connection(
            "wss://193.200.173.45/Auth",
            header=headers,
            sslopt={"cert_reqs": ssl.CERT_NONE}
        )
        ws.send(json.dumps(data0))
        result = ws.recv()
        ws.close()
        
        decoded_data = gzip.decompress(result).decode('utf-8')
        
        if '"comment":"Exists"' in decoded_data:
            failed += 1
            return False
        elif '"status":"Success"' in decoded_data:
            created += 1
            # إرسال إشعار إلى تليجرام عند النجاح
            if bot_token and chat_id:
                requests.get(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    params={"chat_id": chat_id, "text": telegram_message}
                )
            return True
        elif '"comment":"Retry"' in decoded_data:
            failed += 1
            return False
        else:
            # حالة غير معروفة
            failed += 1
            return False
    except Exception as e:
        failed += 1
        return False

def print_stats():
    """عرض الإحصائيات بشكل متجدد"""
    while running:
        sys.stdout.write(f"\r{Fore.GREEN}Created: {created}  {Fore.RED}Failed: {failed}  {Fore.CYAN}Total: {created+failed}{Style.RESET_ALL}")
        sys.stdout.flush()
        sleep(0.5)

def main():
    global running, created, failed
    
    print(Fore.YELLOW + "[*] Safeum Account Generator" + Style.RESET_ALL)
    print(Fore.RED + "⚠️  This module is for educational purposes only. Use responsibly." + Style.RESET_ALL)
    
    # إدخال بيانات تليجرام
    chat_id = input(Fore.MAGENTA + "Enter Telegram chat ID: " + Style.RESET_ALL).strip()
    bot_token = input(Fore.MAGENTA + "Enter Telegram bot token: " + Style.RESET_ALL).strip()
    
    if not chat_id or not bot_token:
        print(Fore.RED + "❌ Chat ID and Bot Token are required." + Style.RESET_ALL)
        return
    
    # إدخال عدد الخيوط
    try:
        threads = int(input(Fore.MAGENTA + "Enter number of threads (default 100): " + Style.RESET_ALL) or "100")
        if threads < 1:
            threads = 1
    except:
        threads = 100
    
    print(Fore.GREEN + f"\n[+] Starting generator with {threads} threads..." + Style.RESET_ALL)
    print(Fore.CYAN + "Press Ctrl+C to stop.\n" + Style.RESET_ALL)
    
    # إعادة تعيين العدادات
    created = 0
    failed = 0
    running = True
    
    # تشغيل خيط عرض الإحصائيات
    stats_thread = threading.Thread(target=print_stats, daemon=True)
    stats_thread.start()
    
    # استخدام ThreadPoolExecutor للتنفيذ المتوازي
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=threads)
    futures = []
    
    try:
        while running:
            # إرسال المهام باستمرار
            futures.append(executor.submit(create_account, bot_token, chat_id))
            # نتحكم بعدد المهام المتراكمة
            if len(futures) > threads * 10:
                # ننتظر بعض المهام لتكتمل
                concurrent.futures.wait(futures[:threads], return_when=concurrent.futures.FIRST_COMPLETED)
                futures = [f for f in futures if not f.done()]
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[!] Stopping... Please wait for current tasks to finish." + Style.RESET_ALL)
        running = False
        executor.shutdown(wait=True, cancel_futures=True)
    
    print(Fore.GREEN + f"\n\n[+] Final Stats - Created: {created}, Failed: {failed}, Total: {created+failed}" + Style.RESET_ALL)
    input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
