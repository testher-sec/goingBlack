from netaddr import IPNetwork
import socket

ip_address = "192.168.112.3"

if ip_address in IPNetwork("192..168.112.0/24"):
    print True


for ip in IPNetwork("192.168.112.1/24"):
    try:
        s = socket.socket()
        s.connect((ip, 25))
        # send mail packets
    finally:
        s.close()