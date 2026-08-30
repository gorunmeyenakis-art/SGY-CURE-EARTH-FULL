import os, time

def main():
    while True:
        os.system('clear')
        print("=======================================================================")
        print("      SGY-CURE-EARTH-FULL | MASTER KARARGAH KONTROL MERKEZİ v5.0       ")
        print("=======================================================================")
        print("  [1] Canlı HUD & Telemetri İzleme")
        print("  [2] AI CNN & QEC Kuantum Onarım Modülü")
        print("  [3] PQC & Termal HAL Modülü")
        print("  [4] HIL Simülatör & DSN Zamanlayıcı")
        print("  [5] Atmosferik RF Attenuation & Güç Kompanzasyonu")
        print("  [6] C++ Native Cosmos DSP & Cooley-Tukey FFT Modülü")
        print("  [7] C++ NASA Final Socket Server & Telemetry I/O Core")
        print("  [8] OTONOM TAM PIPELINE EXECUTION & GIT PUSH")
        print("  [0] Çıkış")
        print("=======================================================================")
        
        c = input("\nSeçiminiz [0-8]: ").strip()
        if c == '1': os.system('python3 sgy_cure_earth_hud.py')
        elif c == '2': os.system('python3 sgy_ai_qec_core.py')
        elif c == '3': os.system('python3 sgy_pqc_hardware_core.py')
        elif c == '4': os.system('python3 sgy_hil_dsn_core.py')
        elif c == '5': os.system('python3 sgy_planetary_rf_core.py')
        elif c == '6': os.system('python3 sgy_cosmos_cpp_core.py')
        elif c == '7': os.system('python3 sgy_nasa_final_core.py')
        elif c == '8':
            os.system('python3 sgy_ai_qec_core.py && python3 sgy_pqc_hardware_core.py && python3 sgy_hil_dsn_core.py && python3 sgy_planetary_rf_core.py && python3 sgy_cosmos_cpp_core.py && python3 sgy_nasa_final_core.py')
            os.system('git add . && git commit -m "feat: added NASA final socket transmitter and telemetry logger core" && git push origin main')
        elif c == '0': break
        input("\nDevam etmek için Enter...")

if __name__ == "__main__": main()
