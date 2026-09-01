#!/usr/bin/env python3
import time
import random

class FusionReactorSim:
    def __init__(self):
        self.target_temp = 150_000_000  # 150 Milyon °C
        self.sun_core_temp = 15_000_000 # Güneş Çekirdeği (15 Milyon °C)
        self.plasma_confined = True

    def run_fusion_cycle(self):
        print("==================================================")
        print("   SGY-NEXUS FUSION PLASMA REACTOR SIMULATION     ")
        print("==================================================")
        print(f"[*] Hedef Plazma Sıcaklığı: {self.target_temp:,} °C")
        print(f"[*] Güneş Çekirdeği Karşılaştırma: {self.sun_core_temp:,} °C (10x Katı)")
        print("[*] Yakıt: Döteryum (D) + Trityum (T) İzotopları\n")

        current_temp = 25_000_000
        for cycle in range(1, 6):
            current_temp += 25_000_000
            magnetic_field_tesla = round(random.uniform(5.1, 5.8), 2)
            fusion_energy_output_mw = round((current_temp / self.target_temp) * 500, 2)
            
            print(f"[Döngü {cycle}/5] Plazma Sıcaklığı: {current_temp:,} °C | Manyetik Hapsedme: {magnetic_field_tesla} T")
            
            if current_temp >= self.target_temp:
                print("\n[+] BARIYER AŞILDI: Pozitif yük itme kuvveti yenildi!")
                print(f"[+] Çekirdek Füzyonu Gerçekleşti. Üretilen Enerji: {fusion_energy_output_mw} MW")
                print("[+] Plazma duvarlara temas etmeden manyetik alanda sabit tutuldu.")
            time.sleep(0.8)

if __name__ == "__main__":
    reactor = FusionReactorSim()
    reactor.run_fusion_cycle()
