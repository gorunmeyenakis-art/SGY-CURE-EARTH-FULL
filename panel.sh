#!/bin/bash
clear
echo "==============================================="
echo "    NASA DEEP SPACE COMMAND CENTER - TERMUX   "
echo "==============================================="
echo "1) Simulate Mars Telemetry Pipeline"
echo "2) Simulate Venus Heavy Ion Probe Link"
echo "3) Simulate Titan Sub-surface Drone Link"
echo "4) System Diagnostics & Exit"
echo "==============================================="
read -p "Select Mission Configuration (1-4): " choice

case $choice in
  1) ./cosmos_core MARS 15.0 8.4 ;;
  2) ./cosmos_core VENUS 45.0 32.0 ;;
  3) ./cosmos_core TITAN 100.0 5.8 ;;
  4) echo "Exiting Command Center Safely."; exit 0 ;;
  *) echo "Invalid Selection."; ./panel.sh ;;
esac
