import subprocess
import socket
import threading
import time
import http.server
import socketserver
import os

def get_local_ip():
    """Get local IP address"""
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
    """Share file using termux-share"""
    try:
        subprocess.run(['termux-share', filepath], check=True)
        return True
    except:
        return False

def start_http_server(directory, port=8080):
    """Start HTTP server in a separate thread"""
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd

def stop_http_server(httpd):
    """Stop HTTP server"""
    httpd.shutdown()
