import sqlite3
import time
import math

class PlanetarySignalSimulator:
    """
    Atmosferik sinyal sönümlemesi ve RF Transceiver güç kompanzasyonu
    donanım simülatörü.
    """
    def __init__(self):
        self.max_tx_power_mw = 50000 # 50 Watt Donanım Sınırı
        self.planet_db = {
            "MARS":  {"name": "Mars",  "alpha": 0.05, "pressure": 0.01},
            "VENUS": {"name": "Venus", "alpha": 4.85, "pressure": 92.0},
            "TITAN": {"name": "Titan", "alpha": 0.35, "pressure": 1.5}
        }

    def calculate_loss(self, planet_key, dist_km, freq_ghz):
        if planet_key not in self.planet_db:
            return 0.0
        prof = self.planet_db[planet_key]
        freq_scale = (freq_ghz / 10.0) ** 2.1
        dynamic_alpha = prof["alpha"] * (prof["pressure"] * freq_scale)
        return 4.343 * dynamic_alpha * dist_km

    def compensate_power(self, planet_key, dist_km, freq_ghz):
        loss_db = self.calculate_loss(planet_key, dist_km, freq_ghz)
        base_power_mw = 500
        mult = 10.0 ** (loss_db / 10.0) if loss_db < 300 else 1e30 # Overflow koruması
        target_power = base_power_mw * mult

        hardware_alert = False
        if target_power > self.max_tx_power_mw:
            hardware_alert = True
            applied_power_mw = self.max_tx_power_mw
        else:
            applied_power_mw = int(target_power)

        return {
            "planet": planet_key,
            "loss_db": round(loss_db, 2),
            "alert": hardware_alert,
            "tx_power_mw": applied_power_mw
        }

class ExoPlanetaryLinkAnalyzer:
    """
    Yüksekliğe bağlı üstel gaz yoğunluğu ve entegral kayıp analizcisi.
    """
    def __init__(self):
        self.atmospheres = {
            "Mars": (0.02, 11.1),
            "Venus": (65.0, 15.9),
            "Titan": (5.3, 21.0)
        }

    def analyze_profile(self, planet, freq_ghz=32.0):
        if planet not in self.atmospheres:
            return 0.0, "UNKNOWN"
        density, scale_h = self.atmospheres[planet]
        freq_penalty = (freq_ghz / 8.4) ** 1.8
        
        # 0km - 100km arası 10 katmanda entegral yaklaşımı
        total_loss = 0.0
        step = 10.0 # km
        for alt in range(0, 100, 10):
            cur_density = density * math.exp(-alt / scale_h)
            alpha_layer = 0.1 * cur_density * freq_penalty
            total_loss += alpha_layer * step

        command = "DEPLOY_SUBORBITAL_RELAY" if total_loss > 40.0 else "LINK_SECURE"
        return round(total_loss, 2), command

def run_planetary_rf_pipeline():
    print("=== SGY-CURE-EARTH | PLANETARY ATMOSPHERIC RF CORE ===")

    # 1. Mars & Venüs RF Kompanzasyon Testi
    sim = PlanetarySignalSimulator()
    mars_res = sim.compensate_power("MARS", 15.0, 8.4)
    venus_res = sim.compensate_power("VENUS", 45.0, 32.0)

    print(f"[✓ RF MARS] Kayıp: {mars_res['loss_db']} dB | Transceiver Gücü: {mars_res['tx_power_mw']} mW | Donanım Sınırı: {mars_res['alert']}")
    print(f"[✓ RF VENÜS] Kayıp: {venus_res['loss_db']} dB | Transceiver Gücü: {venus_res['tx_power_mw']} mW | HARDWARE ALERT: {venus_res['alert']}")

    # 2. Katman Entegral Kayıp Analizi
    analyzer = ExoPlanetaryLinkAnalyzer()
    v_loss, v_cmd = analyzer.analyze_profile("Venus")
    t_loss, t_cmd = analyzer.analyze_profile("Titan")
    print(f"[✓ ATMOSPHERE LINK] Venüs Toplam Kayıp: {v_loss} dB -> Karar: {v_cmd}")
    print(f"[✓ ATMOSPHERE LINK] Titan Toplam Kayıp: {t_loss} dB -> Karar: {t_cmd}")

    # 3. Veritabanı Kaydı
    conn = sqlite3.connect("sgy_nexus_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS planetary_rf_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            mars_loss_db REAL,
            venus_loss_db REAL,
            venus_command TEXT
        )
    ''')
    c.execute('''
        INSERT INTO planetary_rf_logs (timestamp, mars_loss_db, venus_loss_db, venus_command)
        VALUES (?, ?, ?, ?)
    ''', (time.time(), mars_res['loss_db'], v_loss, v_cmd))
    conn.commit()
    conn.close()
    print("[✓ VERİTABANI] Atmosferik RF metrikleri 'sgy_nexus_data.db' Veri Tabanına Yazıldı.\n")

if __name__ == "__main__":
    run_planetary_rf_pipeline()
