import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# إعدادات
OUTPUT_DIR = "reports"
IDENTITIES_DIR = "identities"

# إنشاء المجلدات
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IDENTITIES_DIR, exist_ok=True)