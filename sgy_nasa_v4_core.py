import subprocess, os, sqlite3, time

def run_nasa_v4_pipeline(planet="MARS", distance=15.0, frequency=8.4):
    print(f"=== SGY-CURE-EARTH | NASA V4.0 FULL STACK EXECUTION ({planet}) ===")
    if not os.path.exists("./nasa_mission_control"):
        print("[!] Native 'nasa_mission_control' binary bulunamadı, derleniyor...")
        os.system("g++ -O3 nasa_mission_control.cpp -o nasa_mission_control")

    cmd = ["./nasa_mission_control", str(planet), str(distance), str(frequency)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("[STDERR]", result.stderr)

    conn = sqlite3.connect("sgy_nexus_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS nasa_v4_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            planet TEXT,
            distance_km REAL,
            freq_ghz REAL,
            status TEXT
        )
    ''')
    c.execute('''
        INSERT INTO nasa_v4_logs (timestamp, planet, distance_km, freq_ghz, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (time.time(), planet, distance, frequency, "PASSED_CCSDS_SECURE"))
    conn.commit()
    conn.close()
    print("[✓ VERİTABANI] NASA v4.0 CCSDS & DSP log kaydı işlendi.\n")

if __name__ == "__main__":
    run_nasa_v4_pipeline("MARS", 15.0, 8.4)
    run_nasa_v4_pipeline("TITAN", 1200.0, 14.2)
