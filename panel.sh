#!/bin/bash
# NASA Ultimate Command Center and Automated Log Viewer for Termux

if [ ! -f "./nasa_final_core" ]; then
    echo "[COMPILER] Compiling definitive unified space core system..."
    clang++ -O3 -std=c++11 nasa_final_core.cpp -o nasa_final_core
fi

clear
echo -e "\033[1;33m========================================================\033[0m"
echo -e "\033[1;36m       NASA CENTRAL TELEMETRY AND NETWORKING PANEL      \033[0m"
echo -e "\033[1;33m========================================================\033[0m"
echo " 1) Dispatch Pipeline: Target MARS (8.4 GHz)"
echo " 2) Dispatch Pipeline: Target VENUS (32.0 GHz)"
echo " 3) Dispatch Pipeline: Target TITAN (5.8 GHz)"
echo " 4) View Production Telemetry Logs (cat nasa_mission_telemetry.log)"
echo " 5) Shutdown Mission System"
echo -e "\033[1;33m========================================================\033[0m"
read -p "Execute Sector Code (1-5): " select

case $select in
    1) ./nasa_final_core MARS 15.0 8.4 ;;
    2) ./nasa_final_core VENUS 45.0 32.0 ;;
    3) ./nasa_final_core TITAN 100.0 5.8 ;;
    4) 
        clear
        echo "=== EXPANDING HISTORICAL TELEMETRY LOG FILES ==="
        cat nasa_mission_telemetry.log
        echo "================================================"
        read -p "Press Enter to return to main dashboard..."
        ./panel.sh
        ;;
    5) 
        echo "Disengaging terminal telemetry relays. System Safe."
        exit 0 
        ;;
    *) 
        echo "Unrecognized routing protocol."
        sleep 1
        ./panel.sh
        ;;
esac
