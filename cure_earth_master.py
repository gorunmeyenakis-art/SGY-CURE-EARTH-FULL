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
    
    run_step("Veri Merkezi Kripto Güvenlik Vault", "python3 secure_vault.py")
    time.sleep(1)
    run_step("Flipper Zero & Sub-GHz Sinyal Analizörü", "python3 flipper_subghz.py")
    time.sleep(1)
    run_step("5G CPE & OpenWRT Yönlendirici Yöneticisi", "python3 openwrt_5g_manager.py")
    time.sleep(1)
    run_step("CMOS APS Sensör & LoRA Mesh Analizörü", "python3 cmos_loramesh_analyzer.py")
    time.sleep(1)
    run_step("PLC & RF Haberleşme Modülü", "python3 cure_earth_core.py")
    time.sleep(1)
    run_step("Sensör Teşhis ve Log Analizi", "python3 sensor_logger.py")

    print("\n==================================================")
    print(" [✓] TÜM HARDWARE, SENSÖR VE MESH KATMANLARI SENKRONİZE")
    print("==================================================")

if __name__ == "__main__":
    main()
