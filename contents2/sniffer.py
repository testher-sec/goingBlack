import os
import socket

# host to listen on
host = "192.168.0.104"

# create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host,0)) # interesting, we bind in port 0 :)

# we want the iP headers included in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
# sniffer.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1) # I thought it should be this
# difference between SOL_IP AND IPPROTO_IP

# IF WE ARE USING WINDOWS WE NEED TO SEND AN IOCTL
# to set up promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# read in a sigle packet
print sniffer.recvfrom(65565)

# if we're using Windows, turn off promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
