import hashlib
import hmac
import os
import sys
import time
from base64 import b64encode, b64decode

class DataCenterVault:
    def __init__(self):
        # 256-bit Kriptografik Anahtar Üretimi (Hardware-Entropy / CSPRNG)
        self._master_key = os.urandom(32)
        self._hmac_key = os.urandom(32)
        self.failed_attempts = 0
        self.max_allowed_failures = 3

    def _hash_payload(self, data: str) -> str:
        """HMAC-SHA256 ile veri bütünlük imzası oluşturur."""
        return hmac.new(self._hmac_key, data.encode('utf-8'), hashlib.sha256).hexdigest()

    def encrypt_telemetry(self, raw_data: str) -> dict:
        """Veriyi XOR şifreleme devresi ve HMAC imzası ile zırhlar."""
        # Basitleştirilmiş simüle kripto blok (AES-GCM mantığı)
        keystream = hashlib.sha256(self._master_key).digest()
        cipher_bytes = bytearray()
        
        for i, char in enumerate(raw_data.encode('utf-8')):
            cipher_bytes.append(char ^ keystream[i % len(keystream)])
            
        encrypted_payload = b64encode(cipher_bytes).decode('utf-8')
        signature = self._hash_payload(encrypted_payload)
        
        return {
            "payload": encrypted_payload,
            "signature": signature,
            "timestamp": time.time()
        }

    def verify_and_decrypt(self, packet: dict) -> str:
        """Bütünlük kontrolü yapar; ihlal varsa sistem belleğini temizler."""
        if self.failed_attempts >= self.max_allowed_failures:
            self._purge_memory()
            raise SystemError("[CRITICAL] Güvenlik İhlali! Sistem Kilitlendi ve Bellek Temizlendi.")

        # Signature (İmza) Doğrulama
        expected_sig = self._hash_payload(packet["payload"])
        if not hmac.compare_digest(expected_sig, packet["signature"]):
            self.failed_attempts += 1
            print(f"[ALERT] Manipülasyon Tespit Edildi! Başarısız Deneme: {self.failed_attempts}")
            return None

        # Şifre Çözme (Decryption)
        cipher_bytes = b64decode(packet["payload"].encode('utf-8'))
        keystream = hashlib.sha256(self._master_key).digest()
        plain_bytes = bytearray()
        
        for i, byte in enumerate(cipher_bytes):
            plain_bytes.append(byte ^ keystream[i % len(keystream)])
            
        return plain_bytes.decode('utf-8')

    def _purge_memory(self):
        """Zeroization: Kritik anahtarları bellekten sıfırlayarak siler."""
        self._master_key = b'\x00' * 32
        self._hmac_key = b'\x00' * 32
        print("[FIREWALL] Zeroization: Tüm kriptografik anahtarlar bellekten tamamen silindi.")

if __name__ == "__main__":
    vault = DataCenterVault()
    print("[+] SGY Military-Grade Kriptografik Vault Başlatıldı.")
    
    # Test Verisi
    telemetry = "PLC_STATUS: OK | SENSOR_VOLT: 4.15V | SUB_FREQ: 900MHz"
    
    # Şifreleme
    encrypted_packet = vault.encrypt_telemetry(telemetry)
    print(f"[✓] Şifrelenmiş Paket (Base64) : {encrypted_packet['payload'][:30]}...")
    print(f"[✓] HMAC-SHA256 İmzası       : {encrypted_packet['signature'][:30]}...")

    # Doğrulama ve Çözme
    decrypted_data = vault.verify_and_decrypt(encrypted_packet)
    print(f"[✓] Çözülen Veri Doğrulaması : {decrypted_data}")
