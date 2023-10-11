import socket
import time
import os
import subprocess
import platform
import psutil

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
        self.password = None

        self.target_ssid = target_ssid
        ip = None
        # get ip automatically
        # self.server = socket.gethostbyname(socket.gethostname()) # 192.168.4.2
    

        # Port Number
        self.port = port

        self.server_socket = None
        self.conn = None
        self.addr = None

        self.msg = ""

    def _get_available_ip(self):
        gateway_ip = None
        
        # Get all network interfaces
        interfaces = psutil.net_if_addrs()

        for interface,addresses in interfaces.items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    if "192.168" in address.address:
                        try:
                            return address.address
                        except KeyError:
                            print(f"Error no gateway infomration available")

        return None

    """ Start server and listen for connections """
    def start(self):
        # look for wifi
        self._find_ssid()

        # get IP addresses associated with local machine
        source_ip = self._get_available_ip()
        # TCP tuple
        self.esp = (source_ip,self.port)

        # create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(10)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server_socket.bind(self.esp)

        # listen for connections
        self.server_socket.listen()
        print(f"[LISTENING] Server is listening on  {self.server_socket}:{self.port}")
        # Accept the connection
        try:
            self.conn, self.addr = self.server_socket.accept()
            print(f"[NEW CONNECTION] {self.addr} connected.")
        except TimeoutError as e:
            print(f"Timeout Error - unable to connect")
        time.sleep(1)

    def _find_ssid(self):
        sys = platform.system()

        if sys == "Windows":
            # Windows uses the "netsh" command to connect to Wi-Fi networks
            connect_command = f'netsh wlan connect name="{self.target_ssid}"'
            if not self.password:
                self.password = input('type ssid password:')
            if self.password:
                connect_command += f' keyMaterial="{self.password}"'
            subprocess.run(connect_command, shell=True)

        elif sys == "Linux":
            # Linux uses the "nmcli" command to connect to Wi-Fi networks
            connect_command = f'nmcli dev wifi connect "{self.target_ssid}"'
            if not self.password:
                self.password = input('type ssid password:')
            if self.password:
                connect_command += f' password "{self.password}"'
            subprocess.run(connect_command, shell=True)
        
        else:
            print(f"platform not found")

        # wait X seconds to connect
        for i in range(10):
            time.sleep(1)
            print(".",end="")
        print("")


    def close(self):
        self.server_socket.close()
        system = platform.system()

        if system == "Windows":
            # Windows uses the "netsh" command to disconnect from Wi-Fi networks
            disconnect_command = f'netsh wlan disconnect interface="Wi-Fi" ssid="{self.target_ssid}"'
            subprocess.run(disconnect_command, shell=True)

        elif system == "Linux":
            # Linux uses the "nmcli" command to disconnect from Wi-Fi networks
            disconnect_command = f'nmcli dev disconnect iface "wlp2s0" ssid "{self.target_ssid}"'
            subprocess.run(disconnect_command, shell=True)

        else:
            print("Unsupported operating system")
            return

        print(f"Disconnecting from SSID '{self.target_ssid}'...")
        time.sleep(2)  # Wait for a few seconds for the disconnect to take effect
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
