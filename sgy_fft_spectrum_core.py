import sqlite3
import json
import time
import math
import random

# --- 1. COOLEY-TUKEY RADIX-2 FFT ALGORİTMASI (SAF PYTHON) ---
def execute_cooley_tukey_fft(signal_array):
    """
    C++ Cooley-Tukey Radix-2 FFT mimarisinin saf Python uyarlaması.
    Bit-Reversal Permütasyonu ve Kelebek Operasyonu içerir.
    """
    n = len(signal_array)
    # Diziyi kompleks sayılara dönüştür
    a = [complex(x, 0.0) if not isinstance(x, complex) else x for x in signal_array]

    # 1. Bit-Reversal Permütasyonu
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    # 2. Kelebek (Butterfly) Operasyonu
    length = 2
    while length <= n:
        angle = -2 * math.pi / length
        wlen = complex(math.cos(angle), math.sin(angle))
        
        for i in range(0, n, length):
            w = complex(1.0, 0.0)
            for k in range(length // 2):
                u = a[i + k]
                v = a[i + k + length // 2] * w
                a[i + k] = u + v
                a[i + k + length // 2] = u - v
                w *= wlen
        length <<= 1

    return a

# --- 2. HAREKAT & SPEKTRUM ANALİZ PIPELINE ---
class SGYCosmicSpectrumAnalyzer:
    def __init__(self, signal_size=1024, threshold=15.5):
        self.signal_size = signal_size
        self.threshold = threshold
        self.db_name = "sgy_nexus_data.db"

    def generate_raw_voltage_stream(self):
        # Zamana bağlı voltaj dalgalanmaları (Time-Domain)
        # Rasgele gürültü + Belirli bir frekansta yapay sinyal spike'ı simülasyonu
        stream = [random.gauss(0, 1.0) for _ in range(self.signal_size)]
        # Frekans 128 noktasına yapay dar bantlı sinyal ekleme
        for i in range(self.signal_size):
            stream[i] += 2.5 * math.sin(2 * math.pi * 128 * i / self.signal_size)
        return stream

    def process_and_analyze(self):
        print("=== SGY-CURE-EARTH | FFT SPEKTRUM ANALİZ MOTORU ===")
        print(f"[+] Time-Domain Veri Toplanıyor (Boyut: {self.signal_size})...")
        
        raw_stream = self.generate_raw_voltage_stream()
        
        # 3. ADIM: FFT ile Frekans Alanına Geçiş (Frequency-Domain)
        t_start = time.time()
        fft_output = execute_cooley_tukey_fft(raw_stream)
        execution_time = (time.time() - t_start) * 1000
        
        print(f"[✓ FFT] Radix-2 Dönüşümü Tamamlandı ({execution_time:.2f} ms)")

        # 4. ADIM: Güç Spektrumu Analizi (PSD) ve Yapay Sinyal Tespiti
        detected_signals = []
        print("\n--- SPEKTRUM ANALİZ RAPORU ---")
        for k in range(self.signal_size // 2):  # Simetri nedeniyle yarısı taranır
            magnitude = abs(fft_output[k])
            if magnitude > self.threshold:
                detected_signals.append({"freq_bin": k, "magnitude": round(magnitude, 2)})
                print(f" -> Frekans Bin [{k:4d}] | Sinyal Gücü: {magnitude:6.2f} | [UYARI: YAPAY/AKILLI SİNYAL OLASILIĞI!]")

        # Veritabanına Kaydet
        self.save_to_database(execution_time, len(detected_signals), detected_signals)

    def save_to_database(self, exec_time, signal_count, details):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fft_spectrum_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                fft_size INTEGER,
                exec_time_ms REAL,
                detected_count INTEGER,
                details TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO fft_spectrum_logs (timestamp, fft_size, exec_time_ms, detected_count, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (time.time(), self.signal_size, exec_time, signal_count, json.dumps(details)))
        conn.commit()
        conn.close()
        print(f"\n[✓ VERİTABANI] Spektrum sonuçları '{self.db_name}' veritabanına kaydedildi.\n")

if __name__ == "__main__":
    analyzer = SGYCosmicSpectrumAnalyzer(signal_size=1024, threshold=15.5)
    analyzer.process_and_analyze()
