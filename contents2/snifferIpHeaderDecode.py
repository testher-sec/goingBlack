import socket
import os
import struct
from ctypes import Structure, c_ubyte, c_ushort, c_uint32

'''
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
'''
'''
https://stackoverflow.com/questions/29306747/python-sniffing-from-black-hat-python-book
ctypes work different for 64 and 32 bits system
>>﻿ValueError: Buffer size too small (20 instead of at least 32 bytes)
c_ulong - The problem is with 32 vs 64 bit systems. ------> c_ulong is 4 bytes in i386 and 8 in amd64 <-----------------
    ip_header = IP(raw_buffer[:20]) works on x86 Ubuntu.
    ip_header = IP(raw_buffer[:32]) works on amd64 CentOS 6.6 Python 2.6.6
    ip_header = IP(raw_buffer) works in both.
Change c_ulong to c_uint32
'''

# host to listen on
host = "192.168.0.104"


# our IP header
class IP(Structure):

    # ubyte -> 1 (8)
    # ushort -> 2 (16)
    # ulong -> 4 (32)
    _fields_ = [
        ("ihl",             c_ubyte, 4),
        ("version",         c_ubyte, 4),
        ("tos",             c_ubyte),
        ("len",             c_ushort),
        ("id",              c_ushort),
        ("offset",          c_ushort),
        ("ttl",             c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum",             c_ushort),
        ("src",             c_uint32),
        ("dst",             c_uint32),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer) # what is this? from Structure class?

    def __init__(self, socket_buffer=None):
        # map protocol constants to their names
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        # human redable IP addresses
        # THIS IS BRILLIAN, inet_ntoa VS inet_aton
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))

        # human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

print "Sniffing"

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        #read in a packet
        raw_buffer = sniffer.recv(56565)

        # create an IP header from the first 20 bytes of the buffer
        # ValueError: Buffer size too small (20 instead of at least 32 bytes)... let's try
        ip_header = IP(raw_buffer[0:20])

        #print out the protocol that was detected an d the hosts
        # why are version and header declared in the wrong order?
        #print "Protocol: %s %s -> %s (version %d ihl %d )" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address, ip_header.version, ip_header.ihl)
        print "Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)
#handle CTRL-C
except KeyboardInterrupt:
    # if we are using windows turn off promiscuous mode
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

'''
Bravo! works! :))))
/root/PycharmProjects/Ep2/venv/bin/python /root/PycharmProjects/Ep2/snifferIpHeaderDecode.py
Sniffing
Protocol: ICMP 157.88.129.91 -> 192.168.1.74
Protocol: ICMP 157.88.129.91 -> 192.168.1.74
Protocol: ICMP 157.88.129.91 -> 192.168.1.74
'''