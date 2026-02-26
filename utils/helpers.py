import os
import re
import json
import subprocess
import socket
import threading
import time
import http.server
import socketserver
from datetime import datetime

# الدوال القديمة (تأكد من وجودها)
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^\+?[0-9]{7,15}$'
    return re.match(pattern, phone) is not None

def validate_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(pattern, ip) is not None

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# الدوال الجديدة للمشاركة
def get_local_ip():
    """الحصول على عنوان IP المحلي"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def share_via_termux(filepath):
    """مشاركة الملف باستخدام termux-share"""
    try:
        subprocess.run(['termux-share', filepath], check=True)
        return True
    except:
        return False

def start_http_server(directory, port=8080):
    """تشغيل خادم HTTP في خيط منفصل"""
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd

def stop_http_server(httpd):
    """إيقاف خادم HTTP"""
    httpd.shutdown()
