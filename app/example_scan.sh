#!/bin/bash
# use this as a template to create specific scans

# keep these for your creds and the VPN location
cc=$1
place=$2

# use/update as needed
url=$3

# Leave alone - this connects to the VPN
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
#   Edit this part to do the work - since the rest is setting up the env
#   Put what you want to do in here.  Script?  Cool.  Just a command.  That works too
    echo "Starting ping test now."
    fping $url
fi