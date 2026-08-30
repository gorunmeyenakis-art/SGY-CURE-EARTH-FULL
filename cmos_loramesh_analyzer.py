import sys
import time
import random
import json
from datetime import datetime

class CMOSLoRAMeshAnalyzer:
    def __init__(self, node_id="SGY-MESH-NODE-01"):
        self.node_id = node_id
        self.lora_freq = "868.1 MHz"
        self.mesh_hops = 3  # Mesh ağında aktarılan atlama sayısı

    def capture_cmos_aps_data(self):
        """CMOS Aktif Piksel Sensör matrisinden gürültü ve arka plan radyasyon/ışık piksellerini simüle eder."""
        grid_size = 8  # 8x8 Piksel Matrisi
        pixel_matrix = [[random.randint(0, 1023) for _ in range(grid_size)] for _ in range(grid_size)]
        
        # Olay (Event) Algılama: Eşik değerini aşan piksel sayısı
        threshold = 850
        event_pixels = sum(1 for row in pixel_matrix for val in row if val > threshold)
        
        status = "NORMAL" if event_pixels < 5 else "ANOMALİ DETEKTİ / YÜKSEK ENERJİ OLAYI"
        
        return {
            "matrix_size": f"{grid_size}x{grid_size}",
            "event_count": event_pixels,
            "threshold": threshold,
            "status": status,
            "peak_value": max(max(row) for row in pixel_matrix)
        }

    def process_mesh_routing(self, sensor_payload):
        """LoRA Mesh ağı üzerinden paket kapsülleme ve yönlendirme simülasyonu."""
        route = [self.node_id, "SGY-RELAY-02", "SGY-GATEWAY-MASTER"]
        snr = round(random.uniform(6.0, 12.5), 1)
        rssi = random.randint(-110, -75)
        
        return {
            "origin": self.node_id,
            "route": " -> ".join(route),
            "hops": len(route) - 1,
            "freq": self.lora_freq,
            "rssi_dbm": rssi,
            "snr_db": snr,
            "payload_summary": sensor_payload
        }

    def run_analysis(self):
        print("[+] CMOS APS & LoRA Mesh Haberleşme Analizörü Başlatılıyor...")
        cmos_data = self.capture_cmos_aps_data()
        mesh_packet = self.process_mesh_routing(cmos_data)

        print("=== CMOS APS SENSÖR VE LORA MESH TELEMETRİ RAPORU ===")
        print(f"Kaynak Düğüm   : {mesh_packet['origin']}")
        print(f"Mesh Rotası    : {mesh_packet['route']}")
        print(f"Frekans / Güç  : {mesh_packet['freq']} | {mesh_packet['rssi_dbm']} dBm (SNR: {mesh_packet['snr_db']} dB)")
        print(f"CMOS Matrisi   : {cmos_data['matrix_size']} Piksel")
        print(f"Tepe Değer     : {cmos_data['peak_value']} ADC")
        print(f"Olay Durumu    : {cmos_data['status']} ({cmos_data['event_count']} Piksel Eşik Üstü)")
        print("=======================================================")

if __name__ == "__main__":
    analyzer = CMOSLoRAMeshAnalyzer()
    analyzer.run_analysis()
