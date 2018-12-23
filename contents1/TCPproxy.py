import sys
import socket
import threading


def receive_from(socket):

    buffer = ""

    # we set a 2 second timeout, depending on target this may need adjustment
    socket.settimeout(2)

    try:
        # keep reading into the buffer until there is no more data or we timeout
        while True:
            data = socket.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass # not too escited about this XD

    return buffer


# dump the content of the packet so we can inspect for anything interesting
# from http://code.activestate.com/recipes/142812-hex-dumper/
# pfffff
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length): # start, stop, step
        s = src[i:i + length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X   %-*s   %s" % (i, length * (digits + 1), hexa, text)) #%0 %2 tuple element
    return b'\n'.join(result)


# Modify the packet contents, perform fuzzing tasks, tests for authentication issues or whatever else your heart desires
def response_handler(buffer):
    return buffer


# Modify the packet contents, perform fuzzing tasks, tests for authentication issues or whatever else your heart desires
def request_handler(buffer):
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote host first if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data to send to our local client, send it
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)

    # now let's loop and read from local
    # send to remote
    # read from remote??
    # send to local
    # rinse, wash, repeat

    while True:
        # read from local host
        local_buffer = receive_from(client_socket)

        if len(local_buffer):

            print " [==>] Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)

            # send it to our request handler
            local_buffer = request_handler(local_buffer)

            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print "[==>] Sent to remote."

            # receive back the response
            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):
                print " [==>] Received %d bytes from remote." % len(remote_buffer)
                hexdump(remote_buffer)

                # send to our response handler
                remote_buffer = response_handler(remote_buffer)

                # send the response to the local socket
                client_socket.send(remote_buffer)

                print "[<==] Sent to localhost."

            # This part looks 'funny' to me
            # how are we checking without calling receiving again or even more, without updating the buffers
            # are the buffers being emptied when sent through token?
            # question. to be tested
            # also... why 'or'??
            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print "[*] No more data. Closing connections."

                break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP IPv4

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit(0)

    print "[*] Listening on %s:%d" % (local_host, local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print out the local connectioninformation
        print "[==>] Received incoming connection from %s:%d" % (addr[0],addr[1])

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


if __name__ == '__main__':

    # no fancy command line parsing here
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhos] [localport] [remotehost] [remoteport] [ receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)

    # setup local listening parameters
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    # setup remote target
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # this tells our proxy to connect and receive data
    # before sending to the remote host
    receive_first = sys.argv[5]

    # question. would this work?
    #receive_first = "True" in receive_first.lower()

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # now spin up the listening socket
    # question. do we need all those parameters?
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)