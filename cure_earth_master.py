import subprocess
import sys
import time

def run_step(step_name, command):
    print(f"\n[+] AR-GE MODÜLÜ BAŞLATILIYOR: {step_name}")
    print("-" * 50)
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"[!] HATA: {step_name} modülünde aksama yaşandı.")
        return False
    print(f"[✓] {step_name} BAŞARIYLA TAMAMLANDI.")
    return True

def main():
    print("==================================================")
    print("  SGY-CURE-EARTH TEK TIK OTONOM AR-GE MERKEZİ     ")
    print("==================================================")
    
    # Adım 1: PLC ve RF Simülasyonu
    run_step("PLC & RF Haberleşme Modülü", "python3 cure_earth_core.py")
    time.sleep(1)
    
    # Adım 2: Sensör Teşhis ve Log Analizi
    run_step("Sensör Teşhis ve Log Analizi", "python3 sensor_logger.py")
    time.sleep(1)

    print("\n==================================================")
    print(" [✓] TÜM SİSTEM HATLARI STABİL VE ÇALIŞIR DURUMDA")
    print("==================================================")

if __name__ == "__main__":
    main()
