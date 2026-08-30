import sqlite3
import json
import time
import math
import random

# --- 1. SAF PYTHON BETHE-BLOCH & TERMAL KONTROL SİMÜLATÖRÜ ---
class SatelliteEnvironmentalController:
    """
    Bethe-Bloch enerji kaybi hesabi ve Termal Panjur (Louver)
    donanim kontrol simulatörü.
    """
    def __init__(self):
        self.max_critical_tid = 100.0  # kRad
        self.thermal_min_limit = -40.0 # °C
        self.thermal_max_limit = 85.0  # °C
        self.accumulated_tid_dose = 0.0

    def calculate_bethe_bloch(self, beta=0.85, material_z=14.0):
        if beta <= 0.0 or beta >= 1.0:
            return 0.0
        electron_mass = 0.511 # MeV
        constant_k = 0.307    # MeV cm^2 / mol
        beta_sq = beta * beta
        gamma = 1.0 / math.sqrt(1.0 - beta_sq)
        
        stopping_power = (constant_k * material_z / beta_sq) * (
            math.log((2.0 * electron_mass * beta_sq * gamma * gamma) / 1.0e-4) - beta_sq
        )
        return stopping_power

    def process_environment(self, current_temp, raw_flux):
        # 1. Radyasyon Dozu
        delta_dose = self.calculate_bethe_bloch(0.85, 14.0) * raw_flux * 0.001
        self.accumulated_tid_dose += delta_dose

        tmr_engaged = False
        if self.accumulated_tid_dose > self.max_critical_tid:
            tmr_engaged = True # Triple Modular Redundancy devrede

        # 2. Termal Panjur (Louver) Mantığı
        if current_temp > self.thermal_max_limit:
            louver_state = "100% OPEN (COOLING)"
            heater_state = "OFF"
        elif current_temp < self.thermal_min_limit:
            louver_state = "0% CLOSED (HEATING)"
            heater_state = "PWM 100% ACTIVE"
        else:
            louver_state = "50% BALANCED"
            heater_state = "OFF"

        return {
            "flux": raw_flux,
            "total_tid_krad": round(self.accumulated_tid_dose, 2),
            "tmr_status": tmr_engaged,
            "temp": current_temp,
            "louver": louver_state,
            "heater": heater_state
        }

# --- 2. POST-QUANTUM LATTICE CRYPTO (LWE - SAF PYTHON) ---
class PostQuantumLatticeCrypto:
    """
    Learning With Errors (LWE) tabanli Kuantum-Guvenli
    Kafes Kriptografi Simulatoru.
    """
    def __init__(self, dimension=4, modulus=97):
        self.n = dimension
        self.q = modulus

    def generate_keypair(self):
        s = [random.randint(-1, 1) for _ in range(self.n)]
        A = [[random.randint(0, self.q - 1) for _ in range(self.n)] for _ in range(self.n)]
        e = [random.randint(-1, 1) for _ in range(self.n)]
        
        # t = A*s + e (mod q)
        t = []
        for i in range(self.n):
            val = sum(A[i][j] * s[j] for j in range(self.n)) + e[i]
            t.append(val % self.q)
        return s, (A, t)

    def encrypt_bit(self, public_key, message_bit):
        A, t = public_key
        r = [random.randint(-1, 1) for _ in range(self.n)]
        e1 = [random.randint(-1, 1) for _ in range(self.n)]
        e2 = random.randint(-1, 1)

        # u = A^T * r + e1 (mod q)
        u = []
        for i in range(self.n):
            val = sum(A[j][i] * r[j] for j in range(self.n)) + e1[i]
            u.append(val % self.q)

        # v = t^T * r + e2 + m*(q//2) (mod q)
        m_shift = message_bit * (self.q // 2)
        v_val = sum(t[j] * r[j] for j in range(self.n)) + e2 + m_shift
        v = v_val % self.q

        return u, v

    def decrypt_bit(self, private_key, ciphertext):
        u, v = ciphertext
        s = private_key
        raw_dec = (v - sum(s[i] * u[i] for i in range(self.n))) % self.q
        
        if abs(raw_dec - (self.q // 2)) < (self.q // 4):
            return 1
        return 0

# --- 3. PIPELINE EXECUTION ---
def run_pqc_hardware_pipeline():
    print("=== SGY-CURE-EARTH | DONANIM HAL & PQC KRİPTO ÇEKİRDEĞİ ===")

    # 1. Termal ve Radyasyon Kontrolü
    env = SatelliteEnvironmentalController()
    env_res = env.process_environment(current_temp=92.5, raw_flux=1500.0)
    print(f"[✓ THERMAL/RAD] Sıcaklık: {env_res['temp']}°C | Panjur: {env_res['louver']}")
    print(f"[✓ THERMAL/RAD] Toplam TID Dozu: {env_res['total_tid_krad']} kRad | TMR Devrede: {env_res['tmr_status']}")

    # 2. PQC Kafes Şifreleme (LWE)
    pqc = PostQuantumLatticeCrypto()
    priv_key, pub_key = pqc.generate_keypair()
    bit_to_encrypt = 1 # AI Onaylanmış Sinyal Biti
    cipher = pqc.encrypt_bit(pub_key, bit_to_encrypt)
    decrypted_bit = pqc.decrypt_bit(priv_key, cipher)

    print(f"[✓ PQC KRİPTO] Kaynak Bit: {bit_to_encrypt} -> Şifreli (u, v) Çıktı Üretildi")
    print(f"[✓ PQC KRİPTO] Kuantum-Güvenli Çözülen Bit: {decrypted_bit} (Başarılı: {bit_to_encrypt == decrypted_bit})")

    # 3. Veritabanı Senkronizasyonu
    conn = sqlite3.connect("sgy_nexus_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pqc_hardware_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            temp REAL,
            tid_dose REAL,
            pqc_status TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO pqc_hardware_logs (timestamp, temp, tid_dose, pqc_status)
        VALUES (?, ?, ?, ?)
    ''', (time.time(), env_res['temp'], env_res['total_tid_krad'], "PQC_SUCCESS" if bit_to_encrypt == decrypted_bit else "PQC_FAIL"))
    conn.commit()
    conn.close()
    print("[✓ VERİTABANI] Donanım ve PQC metrikleri 'sgy_nexus_data.db' Veri Tabanına İşlendi.\n")

if __name__ == "__main__":
    run_pqc_hardware_pipeline()
