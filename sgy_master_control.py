import os, time

def main():
    while True:
        os.system('clear')
        print("=======================================================================")
        print("      SGY-CURE-EARTH-FULL | MASTER KARARGAH KONTROL MERKEZİ            ")
        print("=======================================================================")
        print("  [1] Canlı HUD & Telemetri")
        print("  [2] AI CNN & QEC Modülü")
        print("  [3] PQC & Termal/HAL Modülü")
        print("  [4] HIL & DSN Zamanlayıcı Modülü")
        print("  [5] OTONOM TAM PIPELINE EXECUTION & GIT PUSH")
        print("  [0] Çıkış")
        
        c = input("\nSeçiminiz: ").strip()
        if c == '1': os.system('python3 sgy_cure_earth_hud.py')
        elif c == '2': os.system('python3 sgy_ai_qec_core.py')
        elif c == '3': os.system('python3 sgy_pqc_hardware_core.py')
        elif c == '4': os.system('python3 sgy_hil_dsn_core.py')
        elif c == '5':
            os.system('python3 sgy_ai_qec_core.py && python3 sgy_pqc_hardware_core.py && python3 sgy_hil_dsn_core.py')
            os.system('git add . && git commit -m "feat: full deep space AI, QEC, PQC and DSN pipeline integrated" && git push origin main')
        elif c == '0': break
        input("\nDevam etmek için Enter...")

if __name__ == "__main__": main()
