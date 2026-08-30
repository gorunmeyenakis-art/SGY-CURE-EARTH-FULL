import os
import sys
import time

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def main_menu():
    while True:
        clear()
        print("\033[96m\033[1m")
        print("=======================================================================")
        print("      SGY-CURE-EARTH-FULL | MASTER KARARGAH KONTROL MERKEZİ            ")
        print("=======================================================================\033[0m")
        print("  [1] Canlı HUD & Telemetri İzleme (sgy_cure_earth_hud.py)")
        print("  [2] DTN, QKD & Kozmik Nexus Çalıştır (sgy_cosmic_nexus_v6.py)")
        print("  [3] Saf Python Kuantum & AI Çekirdeği (sgy_quantum_ai_core.py)")
        print("  [4] FFT Spektrum & PSD Analiz Motoru (sgy_fft_spectrum_core.py)")
        print("  [5] Tüm Pipeline'ı Sırayla Çalıştır & Otomatik Git Push")
        print("  [0] Çıkış")
        print("\033[92m=======================================================================\033[0m")
        
        choice = input("\033[93mSeçiminiz [0-5]: \033[0m").strip()
        
        if choice == '1':
            os.system('python3 sgy_cure_earth_hud.py')
            input("\nDevam etmek için Enter'a basın...")
        elif choice == '2':
            os.system('python3 sgy_cosmic_nexus_v6.py')
            input("\nDevam etmek için Enter'a basın...")
        elif choice == '3':
            os.system('python3 sgy_quantum_ai_core.py')
            input("\nDevam etmek için Enter'a basın...")
        elif choice == '4':
            os.system('python3 sgy_fft_spectrum_core.py')
            input("\nDevam etmek için Enter'a basın...")
        elif choice == '5':
            cmd = "python3 sgy_cosmic_nexus_v6.py && python3 sgy_quantum_ai_core.py && python3 sgy_fft_spectrum_core.py && python3 sgy_cure_earth_hud.py && git add . && git commit -m 'full execution pipeline complete' && git push origin main"
            os.system(cmd)
            input("\nDevam etmek için Enter'a basın...")
        elif choice == '0':
            print("\033[91mKarargah Oturumu Kapatılıyor...\033[0m")
            break
        else:
            print("Geçersiz seçim!")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
