import sqlite3
import json
import time

def init_and_log_db():
    conn = sqlite3.connect('sgy_nexus_data.db')
    cursor = conn.cursor()
    
    # Tabloyu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cosmic_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            signal_type TEXT,
            channel TEXT,
            metrics TEXT,
            vault_bytes INTEGER
        )
    ''')
    
    # Alınan ve doğrulanan kozmik sinyal verileri
    signals = [
        ("GW150914_GRAVITY", "Spacetime Wave", json.dumps({"strain": 1.023e-21, "energy_solar_mass": 3.0}), 1339),
        ("SUB_GHZ_LORA", "LoRA 868MHz Mesh", json.dumps({"active_nodes": 12, "snr_db": 8.5}), 1339),
        ("MICROWAVE_23G", "23 GHz P2P Link", json.dumps({"loss_db": 118.4, "distance_km": 3.5}), 1339),
        ("CMOS_PARTICLE", "Active Pixel Sensor", json.dumps({"alpha_peaks_per_sec": 42}), 1339),
        ("PMIC_VOLTAGE", "Infineon OPTIREG", json.dumps({"vcc_3v3": 3.304, "status": "STABLE"}), 1339)
    ]
    
    for sig in signals:
        cursor.execute('''
            INSERT INTO cosmic_signals (timestamp, signal_type, channel, metrics, vault_bytes)
            VALUES (?, ?, ?, ?, ?)
        ''', (time.time(), sig[0], sig[1], sig[2], sig[3]))
        
    conn.commit()
    print(f"[✓] {len(signals)} adet kozmik sinyal verisi 'sgy_nexus_data.db' veri tabanına başarıyla yazıldı.")
    conn.close()

if __name__ == "__main__":
    init_and_log_db()
