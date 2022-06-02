#!/bin/bash

cc=$1
place=$2
url=$3
# Check the ip
echo "Checking where we start with."
startFrom=$(curl https://api.myip.com | cut -d "," -f1 | cut -d ":" -f2)
# set DNS first
sh ./setDNS.sh

# now Connect to VPN
openvpn --config configs/$place --auth-user-pass configs/$cc &
#   Needs some time to connect VPN
echo "Giving it a few to connect.  Back in 10 seconds."
sleep 10

# Verify - Let's check the IP again
echo "Checking we don't have the same ip."
connectedTo=$(curl https://api.myip.com | cut -d "," -f1 | cut -d ":" -f2)
echo "Connected to: $connectedTo"
if [ "$connectedTo" == "$startFrom" ]; then
    echo "We aren't connected to the VPN.  Exiting now."
    exit 1
else 
    echo "Starting scan now."
    python3 ./web_scan.py -u $url
fi