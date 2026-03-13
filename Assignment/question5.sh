#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <target_ip> <nse_script>"
    echo "Example: $0 192.168.1.1 http-enum"
    exit 1
fi

TARGET=$1
SCRIPT=$2

if ! command -v nmap &> /dev/null; then
    echo "Error: nmap is not installed."
    exit 1
fi

NSE_PATH=$(nmap --datadir | grep -o '/usr/share/nmap/scripts')
if [ ! -f "${NSE_PATH}/${SCRIPT}.nse" ]; then
    echo "Warning: Script '${SCRIPT}.nse' not found in ${NSE_PATH}. Nmap may fail."
fi

echo "Running Nmap with script '$SCRIPT' on target '$TARGET'..."
nmap -sV -p- --script="$SCRIPT" "$TARGET"