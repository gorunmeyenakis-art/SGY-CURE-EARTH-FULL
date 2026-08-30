import time
import random
import json
from datetime import datetime

class SensorLoggerAnalyzer:
    def __init__(self, log_file="sensor_telemetry.log"):
        self.log_file = log_file
        self.fault_types = ["NORMAL", "GEVSEK_KABLO", "MISCALIBRATION", "SIGNAL_LOSS"]

    def read_raw_sensor(self):
        # Optik/Lazer sensör sinyal simülasyonu (0.0 - 5.0 Volt arası)
        voltage = round(random.uniform(0.0, 5.0), 2)
        
        # Hata teşhis mantığı
        if voltage < 0.5:
            status = "GEVSEK_KABLO"
        elif 0.5 <= voltage < 1.2:
            status = "MISCALIBRATION"
        else:
            status = "NORMAL"
            
        return {"timestamp": datetime.now().isoformat(), "voltage_v": voltage, "status": status}

    def log_event(self, data):
        with open(self.log_file, "a") as f:
            f.write(json.dumps(data) + "\n")

    def run_analysis(self, read_count=10):
        print(f"[+] {read_count} Sensör Okuması Analiz Ediliyor...\n")
        logs = []
        for _ in range(read_count):
            reading = self.read_raw_sensor()
            self.log_event(reading)
            logs.append(reading)
            time.sleep(0.2)
            
        # Analiz Özet Yapısı
        total = len(logs)
        normal_count = sum(1 for l in logs if l['status'] == 'NORMAL')
        fault_count = total - normal_count
        
        print("=== SENSÖR ANALİZ RAPORU ===")
        print(f"Toplam Okuma    : {total}")
        print(f"Stabil Çalışma  : {normal_count}")
        print(f"Hata / Arıza    : {fault_count}")
        print(f"Sağlık Skoru    : %{(normal_count / total) * 100:.1f}")
        print("===========================")

if __name__ == "__main__":
    analyzer = SensorLoggerAnalyzer()
    analyzer.run_analysis(10)
