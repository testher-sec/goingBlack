import paramiko
import threading
import sys
import socket

#using the key from the paramiko demo files
host_key = paramiko.RSAKey(filename='utils/test_rsa.key')


class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == 'kali' and password == 'kali':
            return  paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


if __name__ == '__main__':
    ssh_server = sys.argv[1] # 127.0.0.1
    ssh_port = int(sys.argv[2])

    paramiko.util.log_to_file("filename-serrver.log")
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ssh_server, ssh_port))
        server_socket.listen(100)
        print '[+] Listening for connection...'
        client, addr = server_socket.accept()
    except Exception, e:
        print '[-] Listen failed: ' + str(e)
        sys.exit(1)
    print "[+] Got a connection!"

    # This part could be separated to it's own function. I like leaving less in main one
    # wtf? Am I 'faking' the Transport layer? con dos! :)
    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()
        try:
            bhSession.start_server(server=server)
        except paramiko.SSHException, x:
            print '[-] SSH negotiation failed.'
        chan = bhSession.accept(20)
        print '[+] Authenticated!'
        print chan.recv(1024) # first receive??? for the ClientConnected? or what??
        chan.send('Welcome to bh_ssh')

        while True:
            try:
                command = raw_input("Enter command: ").strip('\n')
                chan.send(command)
                if command != 'exit':
                    print chan.recv(1024) + '\n'
                else:
                    print 'exiting'
                    bhSession.close()
                    raise Exception('exit')
            except KeyboardInterrupt:
                bhSession.close() # finally? :)
    except Exception, e:
        print '[-] Caught exception: ' + str(e)
        try:
            bhSession.close()
        except:
            pass
        sys.exit(1)




