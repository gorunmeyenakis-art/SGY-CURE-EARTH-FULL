import time
import random

class PLCSimulator:
    def __init__(self):
        self.set_reset_latch = False
        self.counter_ctu = 0
        self.max_capacity = 1000

    def process_sensor_input(self, sensor_trigger: bool, emergency_stop: bool):
        if emergency_stop:
            self.set_reset_latch = False
            return "[KRİTİK] Acil Stop Aktif! Sistem Durduruldu."
        
        if sensor_trigger:
            self.set_reset_latch = True
            self.counter_ctu += 1
            return f"[AKTİF] Sinyal Algılandı | Sayıcı (CTU): {self.counter_ctu}"
        return "[BEKLEMEDE] Sensör Sinyali Yok"

class IndustrialRadioComm:
    def __init__(self, frequency_mhz=900):
        self.freq = frequency_mhz

    def send_packet(self, data_payload: str):
        print(f"[RF {self.freq} MHz] Paket 5 km menzilli uzak terminale iletiliyor...")
        time.sleep(0.5)
        return f"[BAŞARILI] Transmit OK -> Payload: {data_payload}"

def main():
    print("==================================================")
    print("   SGY-CURE-EARTH ENDÜSTRİYEL OTOMASYON & KONTROL ")
    print("==================================================")
    
    plc = PLCSimulator()
    radio = IndustrialRadioComm(900)
    
    for cycle in range(1, 6):
        print(f"\n--- Döngü #{cycle} ---")
        sensor_active = random.choice([True, False])
        e_stop = False
        
        status = plc.process_sensor_input(sensor_active, e_stop)
        print(f"PLC Durumu    : {status}")
        
        if plc.set_reset_latch:
            telemetry = f"Döngü:{cycle} | Toplam Ürün:{plc.counter_ctu}"
            rf_status = radio.send_packet(telemetry)
            print(f"Radyo Durumu  : {rf_status}")
            
if __name__ == "__main__":
    main()
