import sqlite3, time, math

class PlanetarySignalSimulator:
    def __init__(self):
        self.max_tx_power_mw = 50000
        self.planet_db = {
            "MARS":  {"name": "Mars",  "alpha": 0.05, "pressure": 0.01},
            "VENUS": {"name": "Venus", "alpha": 4.85, "pressure": 92.0},
            "TITAN": {"name": "Titan", "alpha": 0.35, "pressure": 1.5}
        }

    def calculate_loss(self, planet_key, dist_km, freq_ghz):
        if planet_key not in self.planet_db: return 0.0
        prof = self.planet_db[planet_key]
        freq_scale = (freq_ghz / 10.0) ** 2.1
        dynamic_alpha = prof["alpha"] * (prof["pressure"] * freq_scale)
        return 4.343 * dynamic_alpha * dist_km

    def compensate_power(self, planet_key, dist_km, freq_ghz):
        loss_db = self.calculate_loss(planet_key, dist_km, freq_ghz)
        base_power_mw = 500
        mult = 10.0 ** (loss_db / 10.0) if loss_db < 300 else 1e30
        target_power = base_power_mw * mult
        hardware_alert = target_power > self.max_tx_power_mw
        applied_power_mw = self.max_tx_power_mw if hardware_alert else int(target_power)
        return {"planet": planet_key, "loss_db": round(loss_db, 2), "alert": hardware_alert, "tx_power_mw": applied_power_mw}

class ExoPlanetaryLinkAnalyzer:
    def __init__(self):
        self.atmospheres = {"Mars": (0.02, 11.1), "Venus": (65.0, 15.9), "Titan": (5.3, 21.0)}

    def analyze_profile(self, planet, freq_ghz=32.0):
        if planet not in self.atmospheres: return 0.0, "UNKNOWN"
        density, scale_h = self.atmospheres[planet]
        freq_penalty = (freq_ghz / 8.4) ** 1.8
        total_loss = sum(0.1 * (density * math.exp(-alt / scale_h)) * freq_penalty * 10.0 for alt in range(0, 100, 10))
        command = "DEPLOY_SUBORBITAL_RELAY" if total_loss > 40.0 else "LINK_SECURE"
        return round(total_loss, 2), command

def run_planetary_rf_pipeline():
    sim = PlanetarySignalSimulator()
    mars_res, venus_res = sim.compensate_power("MARS", 15.0, 8.4), sim.compensate_power("VENUS", 45.0, 32.0)
    analyzer = ExoPlanetaryLinkAnalyzer()
    v_loss, v_cmd = analyzer.analyze_profile("Venus")
    conn = sqlite3.connect("sgy_nexus_data.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS planetary_rf_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp REAL, mars_loss_db REAL, venus_loss_db REAL, venus_command TEXT)')
    c.execute('INSERT INTO planetary_rf_logs (timestamp, mars_loss_db, venus_loss_db, venus_command) VALUES (?, ?, ?, ?)', (time.time(), mars_res['loss_db'], v_loss, v_cmd))
    conn.commit()
    conn.close()
    print(f"[✓ PLANETARY RF] Mars Loss: {mars_res['loss_db']} dB | Venus Loss: {v_loss} dB ({v_cmd})")

if __name__ == "__main__": run_planetary_rf_pipeline()
