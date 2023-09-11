import socket
import time
import os
import subprocess
import platform

class PythonServer:

    def __init__(self,
                 HEADER = 64,# Header size
                 FORMAT = "utf-8", # Format of the message
                 DISCONNECT_MESSAGE = "!DISCONNECT", # Disconnection message from the client
                 port= 5050,
                 reqReturnFlag= False,
                 DONECOMMAND = 211,
                 target_ssid="Artus3DTester"):
        
        self.HEADER = HEADER
        self.FORMAT = FORMAT
        self.DISCONNECT_MESSAGE = DISCONNECT_MESSAGE

        self.target_ssid = target_ssid
        
        # get ip automatically
        # self.server = socket.gethostbyname(socket.gethostname()) # 192.168.4.2

        # get ip for specific ssid value
        # windows
        if platform.system() == "Windows":
            try:
                output = subprocess.check_output(['netsh','interface','show','interface'],universal_newlines=True)
                for line in output.splitlines():
                    if self.target_ssid in line:
                        interface = line.split()[0]
                        ip = socket.gethostbyname(socket.gethostbyname)
                        self.ip = ip
            except subprocess.CalledProcessError:
                pass
        elif platform.system == "Linux":
            try:
                output = subprocess.check_output(['iwgetid'], universal_newlines=True)
                if self.target_ssid in output:
                    ip = socket.gethostbyname(socket.gethostname())
                    self.ip = ip
            except subprocess.CalledProcessError:
                pass
        

        # Port Number
        self.port = port
        # TCP tuple
        self.esp = (self.server,self.port)
        self.server_socket = None
        self.conn = None
        self.addr = None

        self.msg = ""

    """ Start server and listen for connections """
    def start(self):
        # create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.esp)

        # listen for connections
        self.server_socket.listen()
        print(f"[LISTENING] Server is listening on  {self.server}:{self.port}")
        # Accept the connection
        self.conn, self.addr = self.server_socket.accept()
        print(f"[NEW CONNECTION] {self.addr} connected.")
        time.sleep(1)

    def close(self):
        self.server_socket.close()
        return 
    
    def receive(self):
         # receive message of 1024 bytes (or an int)
        
        msg = self.conn.recv(200).decode(self.FORMAT) # 193 is byte size of feedback string 
        ## TODO: make sure the packet is complete
        if msg != self.msg:
            self.msg = msg
        return msg
        # return "
    
    def send(self, command):
        # list to str
        # command = ','.join([str(x) for x in command])
        # add a \n at the end of the str
        command =  str(command)
        command += '\n'
        # send encoded data
        # print(command)
        self.conn.send(command.encode(self.FORMAT))
    
    def close(self):
        if self.conn:
            self.conn.close()
        if self.server_socket:
            self.server_socket.close()
        self.conn = None
        self.addr = None
        print("[SERVER CLOSED]")
    
    def flash_wifi(self): 
        acknowledged = False

        file_location = input("Enter file path: ")
        file_size = os.path.getsize(file_location) 

        self.conn.send("file ready\n".encode())
        self.conn.send((str(file_size)+"\n").encode())
        file = open(file_location, "rb")
        file_data = file.read()
        file.close
        self.conn.sendall(file_data)

        while not acknowledged:
            message = self.conn.recv(1024).decode()
            if message == "failed":
                print("File upload failed\n")
                acknowledged = True
            elif message == "success":   
                print("File upload successful\n")
                acknowledged = True

        print("Flashing...")
        
        while True:
            message = self.conn.recv(1024).decode()
            if message == "FLASHED":
                print("Firmware update complete")
                break
    
    def upload_logs_wifi():
        while True:
            # receive here
            if """ finishing condition""":
                break
        return
