from scapy.all import sniff

# our packet callback
def packet_callback(packet):
    print packet.show()

# fire up our sniffer
# if iface parameter not specified, sniff on all interfaces
sniff(prn=packet_callback, count=1)

'''
﻿/root/PycharmProjects/Ep3/venv/bin/python /root/PycharmProjects/Ep3/scapySniffer.py
###[ Ethernet ]### 
  dst       = .................
  src       = .................
  type      = 0x800
###[ IP ]### 
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 202
     id        = 2141
     flags     = 
     frag      = 0
     ttl       = 1
     proto     = udp
     chksum    = 0xfeef
     src       = x.x.x.x
     dst       = x.x.x.x
     \options   \
###[ UDP ]### 
        sport     = 54455
        dport     = 1900
        len       = 182
        chksum    = 0xb157
###[ Raw ]### 
           load      = 'M-SEARCH * HTTP/1.1\r\nHOST: x.x.x.x:1900\r\nMAN: "ssdp:discover"\r\nMX: 1\r\nST: urn:dial-multiscreen-org:service:dial:1\r\nUSER-AGENT: Google Chrome/71.0.3578.98 Mac OS X\r\n\r\n'

None

Process finished with exit code 0

'''