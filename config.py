import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# المسار المباشر لمجلد Download (بعد termux-setup-storage)
BASE_DIR = os.path.expanduser("~/storage/download/7AKM OSINT")

# المجلدات الفرعية
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
IDENTITIES_DIR = os.path.join(BASE_DIR, "identities")

# إنشاء جميع المجلدات
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(IDENTITIES_DIR, exist_ok=True)

print(f"[✓] Files will be saved in: {BASE_DIR}")
