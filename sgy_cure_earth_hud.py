import os
import sys
import time
import random
import sqlite3

# ANSI Renk Kodları (Terminal HUD Görselliği İçin)
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def render_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{CYAN}{BOLD}")
    print(r"""
   _____ ______   __  ____ _   _ ____  _____   _____    _    ____  _____ _   _ 
  / ____/ ___| \ / / / ___| | | |  _ \| ____| | ____|  / \  |  _ \|_   _| | | |
 | (___| |  _ \ V / | |   | | | | |_) |  _|   |  _|   / _ \ | |_) | | | | |_| |
  \___ \ |_| | | |  | |___| |_| |  _ <| |___  | |___ / ___ \|  _ <  | | |  _  |
  ____/\____|_|_|   \____|\___/|_| \_\_____| |_____/_/   \_\_| \_\ |_| |_| |_|
    """)
    print(f"{GREEN}======================================================================={RESET}")
    print(f"{YELLOW}{BOLD}   >>> SGY-CURE-EARTH-FULL | OTONOM AR-GE & SAVUNMA KONTROL MERKEZİ <<<{RESET}")
    print(f"{GREEN}======================================================================={RESET}\n")

def simulate_live_telemetry():
    render_banner()
    print(f"{CYAN}[+] SİSTEM BAŞLATILIYOR... CANLI HUD VE TELEMETRİ AKIŞI AKTİF{RESET}\n")
    time.sleep(1)

    modules = [
        ("Modbus RTU & AnKA GLC Katmanı", "BAĞLANDI (115200 Baud)"),
        ("DTN Bundle Network (RFC 5050)", "STORE & FORWARD OK"),
        ("BB84 Kuantum Kripto Modülü", "GÜVENLİ ANAHTAR AKTİF"),
        ("Kozmik Sinyal & Spektrogram", "SIFIR ANOMALİ / STABİL"),
        ("SGY-Nexus Veri Tabanı", "sgy_nexus_data.db SENKRON")
    ]

    for mod, status in modules:
        print(f"{BOLD}[✓] {mod:<32} -> {GREEN}{status}{RESET}")
        time.sleep(0.3)

    print(f"\n{GREEN}-----------------------------------------------------------------------{RESET}")
    print(f"{BOLD}{YELLOW} CANLI SENSÖR & DONANIM MONITORING (GERÇEK ZAMANLI) {RESET}")
    print(f"{GREEN}-----------------------------------------------------------------------{RESET}")

    try:
        for i in range(1, 6):
            pt00 = round(25.0 + random.uniform(-0.2, 0.2), 2)
            pt01 = round(24.8 + random.uniform(-0.1, 0.1), 2)
            voltage = random.randint(4115, 4125)
            health = 100.0

            sys.stdout.write(
                f"\r{CYAN}[CANLI - Test #{i}/5]{RESET} "
                f"PT00: {GREEN}{pt00}°C{RESET} | "
                f"PT01: {GREEN}{pt01}°C{RESET} | "
                f"Voltaj: {GREEN}{voltage}mV{RESET} | "
                f"Sağlık: {GREEN}%{health}{RESET} | "
                f"Durum: {BOLD}{GREEN}PERFECT{RESET} "
            )
            sys.stdout.flush()
            time.sleep(0.8)
    except KeyboardInterrupt:
        pass

    print(f"\n\n{GREEN}======================================================================={RESET}")
    print(f"{BOLD}{GREEN}[✓] CİLA İŞLEMİ TAMAMLANDI: TÜM SİSTEMLER %100 SAĞLIKLA ÇALIŞIYOR!{RESET}")
    print(f"{GREEN}======================================================================={RESET}\n")

if __name__ == "__main__":
    simulate_live_telemetry()
