import socket

target_host = "127.0.0.1"
target_port = 9999
#
# target_host = "www.google.com"
# target_port = 80

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
client.connect((target_host, target_port))

#send some data
client.send("GET /HTTP/1.1\r\nHost: google.com\r\n\r\n")

#receive some data
response = client.recv(4096)

print response

'''
Assumptions: 
- connection always succeeds
- server always expects us to send data first
- server will send data in a timely fashion
'''