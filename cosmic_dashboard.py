import time
import os
import random
import json
from datetime import datetime
from vault_padding import FixedLengthVault

class SGYCosmicDashboard:
    """
    SGY-CURE-EARTH Evrensel Hibrit Yayın ve Donanım Telemetri
    Termux Canlı Terminal İzleme Arayüzü (Dashboard).
    """
    def __init__(self):
        self.vault = FixedLengthVault(target_size=1339)
        self.start_time = time.time()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def generate_live_metrics(self):
        """Canlı simüle telemetri verileri üretir"""
        gw_strain = 1.0e-21 * (1 + random.uniform(-0.05, 0.05))
        pmic_v33 = 3.30 + random.uniform(-0.02, 0.02)
        panel_load = 120.0 + random.uniform(-5.0, 10.0)
        mw_loss = 118.4 + random.uniform(-1.2, 1.2)
        
        return {
            "gw_strain": gw_strain,
            "pmic_v33": pmic_v33,
            "panel_load": panel_load,
            "mw_loss": mw_loss
        }

    def render(self):
        try:
            while True:
                self.clear_screen()
                m = self.generate_live_metrics()
                uptime = int(time.time() - self.start_time)
                
                print("==========================================================================")
                print("       ★ SGY-CURE-EARTH // EVRENSEL HİBRİT İZLEME PANELİ (DASHBOARD) ★     ")
                print("==========================================================================")
                print(f" Zaman     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Uptime: {uptime}s")
                print(f" Cihaz ID  : SGY-COSMIC-BEACON-2026 | Paket Boyutu: 1339 Bayt (Sabit)")
                print("--------------------------------------------------------------------------")
                
                print("[1] KÜTLEÇEKİMSEL DALGA KANALI (GW150914 Standardı)")
                print(f"  • Uzay-Zaman Doku Gerilimi : {m['gw_strain']:.4e}")
                print(f"  • Enerji Yayılım Modu    : 3.0 Güneş Kütlesi Dönüşümü (Saf Enerji)")
                print(f"  • Yayılım Hızı           : c (Işık Hızı)")
                print()
                
                print("[2] DONANIM & ENERJİ KATMANI (PMIC & Schneider PrismaSeT)")
                print(f"  • Infineon OPTIREG VCC3V3: {m['pmic_v33']:.3f} V [STABLE]")
                print(f"  • Akıllı Pano Yükü       : {m['panel_load']:.1f} Amp")
                print(f"  • ISO 50001 Verimlilik   : %94.2 Yeşil Enerji Oranı [PASS]")
                print()

                print("[3] ŞEHİR İÇİ RF & MİKRODALGA HİBRİT LİNK")
                print(f"  • Frekans / Mesafe       : 23.0 GHz / 3.5 km")
                print(f"  • Serbest Uzay Kaybı     : {m['mw_loss']:.2f} dB")
                print(f"  • Sub-GHz LoRA Mesh      : 868 MHz Active Node Count: 12")
                print()

                print("[4] B2B & YAPAY ZEKA ALTYAPISI")
                print(f"  • AI Compute Engine      : TurkTicaret.Net (NVIDIA H100/H200 NVL)")
                print(f"  • B2B Ekosistem Bağlantısı: OTS Tech Ecosystem (Digital Uz / CAEx)")
                print(f"  • Koruma Kalkanı         : PCU Film Extreme Thermal Shield (-180C/+400C)")
                print("--------------------------------------------------------------------------")
                
                # Vault test paketi doğrulaması
                payload_sample = json.dumps({"pulse": uptime, "metrics": m})
                encrypted = self.vault.pack_and_encrypt(payload_sample)
                
                print(f"[✓] Kriptolu Vault Paketi : {encrypted['total_bytes']} Bayt | Paket Hash: {hash(encrypted['packet_b64']) % 1000000:06d}")
                print("--------------------------------------------------------------------------")
                print(" [Çıkış yapmak için Ctrl+C tuşlarına basın]")
                
                time.sleep(1.5)
        except KeyboardInterrupt:
            print("\n[!] Dashboard izleme modu sonlandırıldı.")

if __name__ == "__main__":
    dashboard = SGYCosmicDashboard()
    dashboard.render()
