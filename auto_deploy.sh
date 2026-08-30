#!/bin/bash
python3 cure_earth_engine.py
python3 cure_earth_master.py

git add .
git commit -m "feat: NetHunter motoru guclendirildi, tam yetki otomasyonu entegre edildi"
git push origin main || git push -u origin main
echo ""
echo "[✓] BAŞARILI: Tüm AR-GE güncellemeleri GitHub repoya aktarıldı!"
