import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# المجلد الرئيسي على الذاكرة الداخلية (بجانب Download)
SHARED_DIR = "/storage/emulated/0/7AKM OSINT"

# المجلدات الفرعية
REPORTS_DIR = os.path.join(SHARED_DIR, "reports")
IDENTITIES_DIR = os.path.join(SHARED_DIR, "identities")

# إنشاء جميع المجلدات إذا لم تكن موجودة
os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(IDENTITIES_DIR, exist_ok=True)

print(f"[✓] Shared directory: {SHARED_DIR}")  # للتأكيد (يمكن إزالته لاحقاً)
