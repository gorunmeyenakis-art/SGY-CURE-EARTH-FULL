#!/bin/bash
# NASA Ultimate Dashboard and Intelligent Node Controller

if [ ! -f "./nasa_ultimate_core" ]; then
    echo "[COMPILER] Compiling Quantum Engine Core with Galactic Signal Intelligence..."
    clang++ -O3 -std=c++11 nasa_ultimate_quantum_core.cpp -o nasa_ultimate_core
fi

clear
echo -e "\033[1;35m========================================================\033[0m"
echo -e "\033[1;32m      NASA COGNITIVE INTERFERENCE & MISSION CONTROL     \033[0m"
echo -e "\033[1;35m========================================================\033[0m"
echo " 1) Boot Space Link to MARS   (Autonomous Band & Technosignature Scan)"
echo " 2) Boot Space Link to VENUS  (Autonomous Band & Technosignature Scan)"
echo " 3) Boot Space Link to TITAN  (Autonomous Band & Technosignature Scan)"
echo " 4) Extract Dynamic Mission Logs (Live View)"
echo " 5) Disengage Command Node"
echo -e "\033[1;35m========================================================\033[0m"
read -p "Execute Choice Vector (1-5): " choice

case $choice in
    1) ./nasa_ultimate_core MARS 15.0 14 ;;
    2) ./nasa_ultimate_core VENUS 45.0 21 ;;
    3) ./nasa_ultimate_core TITAN 100.0 28 ;;
    4) 
        clear
        echo "=== EXPANDING AI-RF COGNITIVE MISSION CHRONICLES ==="
        cat nasa_mission_telemetry.log | tail -n 25
        echo "===================================================="
        read -p "Press Enter to bounce back to operational panel..."
        ./panel.sh
        ;;
    5) 
        echo "NASA Central Operations powered down. Safe mode active."; exit 0 ;;
    *) 
        echo "Protocol deviation detected." ; sleep 1 ; ./panel.sh ;;
esac
