import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# المسار الصحيح للذاكرة الخارجية عبر Termux
BASE_DIR = os.path.expanduser("~/storage/shared")
SHARED_DIR = os.path.join(BASE_DIR, "7AKM OSINT")

# المجلدات الفرعية
REPORTS_DIR = os.path.join(SHARED_DIR, "reports")
IDENTITIES_DIR = os.path.join(SHARED_DIR, "identities")

# إنشاء جميع المجلدات إذا لم تكن موجودة
os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(IDENTITIES_DIR, exist_ok=True)

# تأكيد المسار (اختياري)
print(f"[✓] Shared directory: {SHARED_DIR}")
