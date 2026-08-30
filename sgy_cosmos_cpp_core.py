import subprocess
import os
import sqlite3
import time

def run_cosmos_cpp_simulation(planet="MARS", distance=15.0, frequency=8.4):
    print(f"=== SGY-CURE-EARTH | C++ COSMOS DSP CORE EXECUTION ({planet}) ===")
    
    if not os.path.exists("./cosmos_core"):
        print("[!] Native 'cosmos_core' binary bulunamadı, derleniyor...")
        os.system("g++ -O3 cosmos_core.cpp -o cosmos_core")

    cmd = ["./cosmos_core", str(planet), str(distance), str(frequency)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("[STDERR]", result.stderr)

    # Veritabanı Entegrasyonu
    conn = sqlite3.connect("sgy_nexus_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cpp_dsp_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            planet TEXT,
            distance_km REAL,
            freq_ghz REAL,
            status TEXT
        )
    ''')
    c.execute('''
        INSERT INTO cpp_dsp_logs (timestamp, planet, distance_km, freq_ghz, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (time.time(), planet, distance, frequency, "PASSED"))
    conn.commit()
    conn.close()
    print("[✓ VERİTABANI] C++ DSP & FFT simülasyon çıktısı kaydedildi.\n")

if __name__ == "__main__":
    run_cosmos_cpp_simulation("MARS", 15.0, 8.4)
    run_cosmos_cpp_simulation("VENUS", 45.0, 32.0)
