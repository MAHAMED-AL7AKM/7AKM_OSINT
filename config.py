import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# إعدادات المجلدات
OUTPUT_DIR = "reports"
IDENTITIES_DIR = "identities"
REPORTS_DIR = "reports"   # هذا المتغير المطلوب

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IDENTITIES_DIR, exist_ok=True)
