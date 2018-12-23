import socket

'''
ADD "\r\n" TO THE MESSAGE SENT TO FTP
OTHERWISE DOESNT RETURN RESPONSE
DOESNT UDERSTAND NEW LINE & END OF COMMAND

test.rebex.net
Username is "demo", password is "password"

'''

target_host = "test.rebex.net"
# target_host = "ftp.rediris.es"
target_port = 21
#
# target_host = "127.0.0.1"
# target_port = 2226
#
# target_host = "www.google.com"
# target_port = 80

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
client.connect((target_host, target_port))

response = client.recv(4096)
print "First time... " , response

# message = "HELP\r\n"
# client.send(message)
# print "Sending HELP"
# response = client.recv(4096)
# print "HELP... ", response
#

while True:
    #send some data
    input_data = raw_input("data>>") + "\r\n"
    client.send(input_data)

    #receive some data
    response = client.recv(4096)
    print response

    if not response:
        break

client.close()

'''
Assumptions: 
- connection always succeeds
- server always expects us to send data first
- server will send data in a timely fashion
'''