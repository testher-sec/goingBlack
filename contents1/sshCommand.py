import paramiko

def ssh_command(ip, user, password, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/evega/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    client.close()
    return


ssh_command("192.168.0.102", "kali", "kali", "id")