import serial
import time

class PythonEsp32Serial:

    def __init__(self, port='COM9',
                 baudrate=115200, #115200, 
                 timeout=1):
        
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

    def send(self, data:str):
        self.esp32.write(data.encode('utf-8'))
        # print(len(data.encode('utf-8')))

    def receive(self):
        ## check if something is available to read
        if self.esp32.in_waiting > 100: # receive the message and decode it to utf-8
            data = self.esp32.readline().decode("ISO-8859-1")
            #print(data)
            return str(data)
        return ""
    
    def flash_serial(self):
        print("TO BE IMPLEMENTED...")
        # implement later
        return
    
    def upload_logs_serial(self):
        # receive files here
        return

    def close(self):
        self.esp32.close()
