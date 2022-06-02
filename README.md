### What does this do?

The image takes a script and does what it's told inside the image, that will be connected to the VPN.
The example_scan.sh script should be a good way to get things started.  This runs a ping test.  There is also a nmap example as well as a web crawl.

### Requirements:
Hide My Ass VPN account. This uses openVPN so modify as needed for another VPN provider that uses openVPN for connections.  Should work with them as well.

Docker - not a ton of resources needed

Tested on Debian, OSX, Azure VMs and AWS EC2. Cloud tests were done on the free tiers without issue.


### Setup:
First set up the environment if you haven't already:
```
$ ./makeenv.sh
```
This will create the docker image.

Docker image contains wget, curl, fping, python3, chrome (for screenshots), and nmap

Python requirements includes Beautiful Soup and Selenium

Add the tools that work for you to the image and rerun the image create

Put your HMA account info in app/configs/config.deets

Choose HMA open VPN configs from: https://vpn.hidemyass.com/vpn-config/OpenVPN-2.4/UDP/
Download to app/configs/
Config for NY, NY is supplied for an example

### Examples

Move to the app directory to run these examples.

#### To run a script scan run:
```
docker run \
-it --rm --name webScan -v ${PWD}:/mnt \
--sysctl net.ipv6.conf.all.disable_ipv6=0 --cap-add=NET_ADMIN --device=/dev/net/tun \
hma-base \
./web_scan.sh config.deets USA.NewYork.Manhattan.UDP.ovpn https://themonkeyplayground.com
```
This will run the web_scan.py script against themonkeyplayground.com and provide output gathered

#### To run a command scan:

We have the example_scan.sh that will run a ping test:
```
docker run \
-it --rm --name pingScan -v ${PWD}:/mnt \
--sysctl net.ipv6.conf.all.disable_ipv6=0 --cap-add=NET_ADMIN --device=/dev/net/tun \
hma-base \
./example_scan.sh config.deets USA.NewYork.Manhattan.UDP.ovpn github.com
```
and the Nmap example:
```
docker run \
-it --rm --name nampScan -v ${PWD}:/mnt \
--sysctl net.ipv6.conf.all.disable_ipv6=0 --cap-add=NET_ADMIN --device=/dev/net/tun \
hma-base \
./nmap_scan.sh config.deets USA.NewYork.Manhattan.UDP.ovpn themonkeyplayground.com
```


