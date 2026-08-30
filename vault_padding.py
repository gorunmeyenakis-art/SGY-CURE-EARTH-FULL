import os
import hashlib
import hmac
from base64 import b64encode, b64decode

class FixedLengthVault:
    def __init__(self, target_size=1339):
        self.target_size = target_size
        self._key = os.urandom(32)
        self._hmac_key = os.urandom(32)

    def pack_and_encrypt(self, raw_data: str) -> dict:
        data_bytes = raw_data.encode('utf-8')
        length_header = len(data_bytes).to_bytes(2, byteorder='big')
        payload_with_header = length_header + data_bytes
        
        body_target_size = self.target_size - 50
        if len(payload_with_header) > body_target_size:
            raise ValueError("Veri boyutu sınırı aştı!")
            
        padding_needed = body_target_size - len(payload_with_header)
        padding_bytes = os.urandom(padding_needed)
        padded_body = payload_with_header + padding_bytes
        
        nonce = os.urandom(16)
        formula_id = b'\x41\x42'
        
        keystream = hashlib.sha256(self._key + nonce).digest()
        cipher_body = bytearray()
        for i, b in enumerate(padded_body):
            cipher_body.append(b ^ keystream[i % len(keystream)])
            
        raw_packet = nonce + formula_id + bytes(cipher_body)
        signature = hmac.new(self._hmac_key, raw_packet, hashlib.sha256).digest()
        final_packet = raw_packet + signature
        
        return {
            "packet_b64": b64encode(final_packet).decode('utf-8'),
            "total_bytes": len(final_packet)
        }

    def decrypt_and_unpack(self, packet_b64: str) -> str:
        raw_packet = b64decode(packet_b64)
        if len(raw_packet) != self.target_size:
            raise ValueError("Paket boyutu geçersiz!")
            
        payload_data = raw_packet[:-32]
        received_sig = raw_packet[-32:]
        
        expected_sig = hmac.new(self._hmac_key, payload_data, hashlib.sha256).digest()
        if not hmac.compare_digest(received_sig, expected_sig):
            raise PermissionError("Bütünlük doğrulaması başarısız!")
            
        nonce = payload_data[:16]
        cipher_body = payload_data[18:]
        
        keystream = hashlib.sha256(self._key + nonce).digest()
        plain_body = bytearray()
        for i, b in enumerate(cipher_body):
            plain_body.append(b ^ keystream[i % len(keystream)])
            
        orig_length = int.from_bytes(plain_body[:2], byteorder='big')
        return plain_body[2:2 + orig_length].decode('utf-8')
