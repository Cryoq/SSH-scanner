import paramiko
import pyfiglet
import sys
from queue import Queue
import threading 
import socket

def startup():       
    ascii_banner = pyfiglet.figlet_format("Test Port Scanner")
    print(ascii_banner)
    
def uploadRunScript(ip, localPath, remotePath, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(ip, username=username, password=password)
        '''
        #uploads local script
        sftp = ssh.open_sftp()
        sftp.put(localPath, remotePath)
        sftp.close()
        '''
        remotePath = "/home/$USER/testScript.sh"
        ssh.exec_command(f"chmod +x {remotePath}")
        
        _stdin, _stdout, _stderr = ssh.exec_command(remotePath)
        print(_stdout.read().decode())
        ssh.close()
    except paramiko.AuthenticationException:
        print(f"Authetication failed")
    except paramiko.SSHException as e:
        print(f"Unable to establish connection for {ip}: {e}")
    except Exception as e:
        print(f"Error durring SFTP or exec: {e}")
    
    
    
def portscan(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(.1)
        result = s.connect_ex((ip,port))
        if result == 0:
            print(f"{ip}: Port {port} is open.")
            connections.append(ip)
        s.close()
    except socket.gaierror:
        print("\nHostname couldnt be resolved")
        sys.exit()
    except KeyboardInterrupt:
        print("\nEnding Script")
        sys.exit()
        
def threader():
    while True:
        worker = q.get()
        ip, port = worker
        portscan(ip, port)
        q.task_done()
    
    
startup()   
    
targets = []
user = int(input("1. Specific ip\n2. ip range"))
if user == 1:
    target = input("What ip would you like to test ssh")

if user == 2:
    target = input("What ip range would you like me to scan? ( x.x.x.x/x )")
    x = target.split("/")
    cider = x[1]
    ipNumbers = x[0].split(".")
    print(ipNumbers, cider)
    
    if cider == "24":
        for i in range(256):
            targets.append(f"{ipNumbers[0]}.{ipNumbers[1]}.{ipNumbers[2]}.{i}")
    print(targets)
    
    
q = Queue()
port = 22
connections = []

for i in range(30):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()
    

for _,v in enumerate(targets):
    worker = (v, port)
    q.put(worker)
q.join()

print(f"All ips that i can connect to are {connections}")

username = 'osboxes'
password = 'osboxes.org'
localpath = "C:\\Users\\cryoq\\Downloads\\testScript.sh"
remotePath = "/home/$USER/"
for _,v in enumerate(connections):
    uploadRunScript(v,localpath, remotePath, username, password)
    v