import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key (مشفر)
ENCODED_KEY = "QUl6YVN5Qi1ubnpiYk00MU1LZXpQa1ZVU1M1VVhLbGNBQnVtbUxn"
GEMINI_API_KEY = base64.b64decode(ENCODED_KEY).decode()

# المسار الصحيح للذاكرة الخارجية عبر Termux
BASE_DIR = os.path.expanduser("~/storage/downloads")
SHARED_DIR = os.path.join(BASE_DIR, "7AKM OSINT")

# المجلدات الفرعية
REPORTS_DIR = os.path.join(SHARED_DIR, "reports")
IDENTITIES_DIR = os.path.join(SHARED_DIR, "identities")

# إنشاء جميع المجلدات
os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(IDENTITIES_DIR, exist_ok=True)

print(f"[✓] Files will be saved in: {SHARED_DIR}")
