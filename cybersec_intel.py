#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error
import hashlib

class ThreatIntelFramework:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.api_keys = {"abuseipdb": "", "virustotal": ""}
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.api_keys.update(data.get("api_keys", {}))
        except FileNotFoundError:
            self.save_config()

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump({"api_keys": self.api_keys}, f, indent=4)

    def set_key(self, service, key):
        if service in self.api_keys:
            self.api_keys[service] = key
            self.save_config()
            print(f"[+] {service.upper()} API anahtarı kaydedildi.")
        else:
            print(f"[-] Bilinmeyen servis: {service}")

    def check_urlhaus(self, target):
        print(f"[*] [URLhaus] {target} taranıyor...")
        url = "https://urlhaus-api.abuse.ch/v1/host/"
        data = f"host={target}".encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"User-Agent": "CyberSec-Tool"})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode())
                if res.get("query_status") == "ok":
                    urls = res.get("urls", [])
                    print(f"  [!] UYARI: {len(urls)} adet zararlı URL tespit edildi!")
                else:
                    print("  [+] URLhaus veritabanında zararlı kaydı yok (Temiz).")
        except Exception as e:
            print(f"  [-] URLhaus hatası: {e}")

    def check_abuseipdb(self, ip_address):
        key = self.api_keys.get("abuseipdb")
        if not key:
            print("[!] AbuseIPDB API anahtarı tanımlanmamış!")
            return
        print(f"[*] [AbuseIPDB] IP Sorgulanıyor: {ip_address}")
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip_address}"
        req = urllib.request.Request(url, headers={"Key": key, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode()).get("data", {})
                print(f"  - Şüphe Skoru: %{res.get('abuseConfidenceScore', 0)}")
        except Exception as e:
            print(f"  [-] AbuseIPDB hatası: {e}")

    def scan_file_hash(self, filepath):
        try:
            sha256 = hashlib.sha256()
            with open(filepath, "rb") as f:
                for block in iter(lambda: f.read(4096), b""):
                    sha256.update(block)
            calc_hash = sha256.hexdigest()
            print(f"[*] Dosya SHA256: {calc_hash}")
        except Exception as e:
            print(f"[-] Dosya hatası: {e}")

def main():
    tool = ThreatIntelFramework()
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "domain" and len(sys.argv) > 2:
            tool.check_urlhaus(sys.argv[2])
        elif cmd == "ip" and len(sys.argv) > 2:
            tool.check_abuseipdb(sys.argv[2])
        elif cmd == "file" and len(sys.argv) > 2:
            tool.scan_file_hash(sys.argv[2])
        elif cmd == "set-key" and len(sys.argv) > 3:
            tool.set_key(sys.argv[2], sys.argv[3])
    else:
        tool.check_urlhaus("example.com")

if __name__ == "__main__":
    main()
