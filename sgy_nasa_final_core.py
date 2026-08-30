import subprocess, os, sqlite3, time

def run_nasa_final_pipeline(planet="MARS", distance=15.0, frequency=8.4):
    print(f"=== SGY-CURE-EARTH | NASA FINAL NETWORK & TELEMETRY CORE ({planet}) ===")
    if not os.path.exists("./nasa_final_core"):
        os.system("g++ -O3 nasa_final_core.cpp -o nasa_final_core")

    cmd = ["./nasa_final_core", str(planet), str(distance), str(frequency)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)

    conn = sqlite3.connect("sgy_nexus_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS nasa_final_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            planet TEXT,
            distance_km REAL,
            freq_ghz REAL,
            status TEXT
        )
    ''')
    c.execute('''
        INSERT INTO nasa_final_logs (timestamp, planet, distance_km, freq_ghz, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (time.time(), planet, distance, frequency, "NETWORK_SOCKET_OK"))
    conn.commit()
    conn.close()
    print("[✓ VERİTABANI] Socket ve I/O Log kaydı tamamlandı.\n")

if __name__ == "__main__":
    run_nasa_final_pipeline("MARS", 15.0, 8.4)
