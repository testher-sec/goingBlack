import sys

from utils.arperHelper import restore_target, get_mac

'''
We are having a bit of trouble restoring from ARP poisoning
Let's separate it to its own functionality
'''

target_ip = "192.168.119.11"
gateway_ip = "192.168.119.1"

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print "nooooooo gw mac"
    sys.exit(0)
target_mac = get_mac(target_ip)
if target_mac is None:
    print "nooooooo gw mac"
    sys.exit(0)

restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
