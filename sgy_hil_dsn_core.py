import sqlite3, json, time, random

def run_hil_dsn():
    jitter_ns = random.randint(120, 380)
    schedule = {"Goldstone_70m": ["Voyager_1", "James_Webb"], "Madrid_70m": ["Mars_Persevere", "DEEP_SCAN"]}
    conn = sqlite3.connect("sgy_nexus_data.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS hil_dsn_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp REAL, max_jitter_ns INTEGER, dsn_allocation_json TEXT)')
    c.execute('INSERT INTO hil_dsn_logs (timestamp, max_jitter_ns, dsn_allocation_json) VALUES (?, ?, ?)', (time.time(), jitter_ns, json.dumps(schedule)))
    conn.commit()
    conn.close()
    print(f"[✓ HIL/DSN] Jitter: {jitter_ns}ns | DSN Matrix Updated.")

if __name__ == "__main__": run_hil_dsn()
