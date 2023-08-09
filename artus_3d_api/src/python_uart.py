import serial
import time

class PythonEsp32Serial:

    def __init__(self, port='COM9',
                 baudrate=115200, #115200, 
                 timeout=5):
        
        # automatically connect to the first available port
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        # self.esp32 = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.esp32 = serial.Serial(baudrate=self.baudrate, timeout= self.timeout)

    def start(self):
        self.esp32.port=self.port
        self.esp32.close()
        self.esp32.open()

    def send(self, data):
        self.esp32.write(data.encode())
        #print(data.encode())

    def receive(self):
        ## check if something is available to read
        if self.esp32.in_waiting > 0: # receive the message and decode it to utf-8
            data = self.esp32.readline()
            #print(data)
            return str(data)
        return ""
    
    def upload_serial(self):
        #implement later
        return

    def close(self):
        self.esp32.close()
