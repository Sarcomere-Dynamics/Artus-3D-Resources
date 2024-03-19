from src.ArtusCommunicator import ArtusCommunicator

import serial
import time

class ArtusUART(ArtusCommunicator):

    def __init__(self, port='COM9',
                 baudrate=115200, #115200, 
                 timeout=0.5):
        
        # automatically connect to the first available port
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.esp32 = serial.Serial(baudrate=self.baudrate, timeout= self.timeout)
        super().__init__()
        
        self.timer_send = 0.003
        self.timer_recv = self.timer_send*2

    def start(self):
        self.esp32.port=self.port
        self.esp32.close()
        self.esp32.open()

    def send(self, data:bytearray):
        self.esp32.write(data)
        t = time.perf_counter()
        while time.perf_counter() - t < self.timer_send:
            pass

    def receive(self,data:list):
        # i = 0
        # t = time.perf_counter()
        # while self.esp32.in_waiting < 65:
        #     print(self.esp32.in_waiting)
        #     if time.perf_counter() - t > 0.005:
        #         break
        t = time.perf_counter()
        while time.perf_counter() - t < self.timer_recv:
            pass
        if self.esp32.in_waiting == 65:
            msg_bytes = self.esp32.read(65)
        else:
            msg_bytes = self.esp32.read_all()
            return None

        # ## check if something is available to read
        # while self.esp32.in_waiting > 1:
        #     rb = self.esp32.read()
        #     # case when looking at int16_t values
        #     if 17 <= i <= 47:
        #         rb1 = self.esp32.read()
        #         data[i] = int.from_bytes((rb+rb1),byteorder='little',signed=True)
        #     # general case where looking at single byte values -127 <-> 127
        #     else:
        #         data[i] = int.from_bytes(rb,signed=True)
        #     i+=1
        print('msg length = '+str(len(msg_bytes)))
        if len(msg_bytes) == 65:
            return msg_bytes
            
        return None

    def close(self):
        self.esp32.close()
