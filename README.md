Requirements:
Tested on Debian, OSX, Azure VMs and AWS EC2 instances
Docker

Setup:
First set up the environment if you haven't already:
$ ./makeenv.sh
This will create the docker image.
Docker image contains wget, curl, python3, chrome (for screenshots), and nmap
Python requirements includes Beautiful Soup and Selenium

Add the tools that work for you to the image

Put your HMA account info in app/configs/config.deets as:
username
password

Choose HMA open VPN configs from: https://vpn.hidemyass.com/vpn-config/OpenVPN-2.4/UDP/
Download to app/configs/
Config for NY, NY is supplied for an example

Examples:::

The image takes a script and does what it's told inside the image, that will be connected to the VPN.
The example_scan.sh script should be a good way to get things started.

Examples set up:
To run a script scan run:
docker run \
-it --rm --name webScan -v ${PWD}:/mnt \
--sysctl net.ipv6.conf.all.disable_ipv6=0 --cap-add=NET_ADMIN --device=/dev/net/tun \
hma-base \
./web_scan.sh config.deets USA.NewYork.Manhattan.UDP.ovpn https://themonkeyplayground.com

This will run the web_scan.py script against themonkeyplayground.com and provide output gathered

To run a command scan:

We have the example_scan.sh that will run a ping test:
docker run \
-it --rm --name pingScan -v ${PWD}:/mnt \
--sysctl net.ipv6.conf.all.disable_ipv6=0 --cap-add=NET_ADMIN --device=/dev/net/tun \
hma-base \
./example_scan.sh config.deets USA.NewYork.Manhattan.UDP.ovpn github.com

and the Nmap example:
docker run \
-it --rm --name nampScan -v ${PWD}:/mnt \
--sysctl net.ipv6.conf.all.disable_ipv6=0 --cap-add=NET_ADMIN --device=/dev/net/tun \
hma-base \
./nmap_scan.sh config.deets USA.NewYork.Manhattan.UDP.ovpn themonkeyplayground.com


