from src.Artus3DJoint import Artus3DJoint
from src.ArtusTCP import ArtusTCP
from src.ArtusUART import ArtusUART

import time

# Constants
# communication type
WIFI = 'WiFi'
UART = 'UART'
# commands 
TARGET              = 176
CALIBRATE           = 55
START               = 88
SLEEP               = 25
GETSTATES           = 20
SAVEGRASPONBOARD    = 200
GETGRASPONBOARD     = 210

class ArtusAPI:
    def __init__(self,
                communication_method = WIFI,
                port = 'COM6',
                target_ssid = 'ArtusTester',
                hand = 'right'
                ):
        
        self.target_ssid = target_ssid
        self.communication_method = communication_method
        self.port = port
        self.hand = hand

        self.command = None
        self.ack = None
        self.received_data = [None for _ in range(81)]

        self.default_velocity = 90

        joint_names = ['thumb_flex','thumb_spread','thumb_d2','thumb_d1','index_flex','index_spread','index_d2',
                'middle_flex','middle_spread','middle_d2','ring_flex','ring_spread','ring_d2','pinky_flex',
                'pinky_spread','pinky_d2']

        constraints = {
            'max':[90,35,90,90,90,20,90,90,20,90,90,20,90,90,20,90],
            'min':[0,-35,0,0,0,-20,0,0,-20,0,0,-20,0,0,-20,0]
        }

        self.joints = {}
        for i,joint in enumerate(joint_names):
            self.joints[joint] = Artus3DJoint(joint,i,constraints['max'][i],constraints['min'][i])

        # instantiate communication classes
        if self.communication_method == UART:
            self.communication = ArtusUART(port=port,baudrate=115200)
        else:
            self.communication = ArtusTCP(target_ssid=target_ssid)

    
    def start_connection(self):
        self.communication.start()

    def start_robot(self):
        # RTC start time from PC
        year    = int(time.localtime().tm_year - 2000)
        month   = int(time.localtime().tm_mon)
        day     = int(time.localtime().tm_mday)
        hour    = int(time.localtime().tm_hour)
        minute  = int(time.localtime().tm_min)
        second  = int(time.localtime().tm_sec)

        start_values = [20,year,month,day,hour,minute,second]

        byte_data = self.communication.list_to_bytearray(START,start_values)
        self.communication.send(byte_data)
    
    def calibrate_robot(self):
        byte_data = self.communication.list_to_bytearray(CALIBRATE,[0])
        self.communication.send(byte_data)

    def close_connection(self):
        self.communication.close()

    def send_target_command(self,cmd:dict=None):
        # fix the abduction and adduction
        if self.hand == 'right' and cmd is not None: # do not check constraints on test values
            for name,joint in cmd.items():
                if 'spread' in name:
                    joint.input_angle = -joint.input_angle

            byte_data = self.communication.dict_to_bytearray(cmd,TARGET)

        # fix the abduction and adduction
        elif self.hand == 'right':
            for name,joint in self.joints.items():
                joint.check_input_constraints() # check constraints
                if 'spread' in name:
                    joint.input_angle = -joint.input_angle

            byte_data = self.communication.dict_to_bytearray(self.joints,TARGET)

        self.communication.send(byte_data)
        
    def get_robot_states(self):
        byte_data = self.communication.list_to_bytearray(GETSTATES,[0])
        self.communication.send(byte_data)

        start = time.perf_counter()

        # time.sleep(0.01)
        
        # while self.communication.receive(self.received_data) is None:
        #     if time.perf_counter() - start > 0.002:
        #         return None
        self.received_data = self.communication.receive(self.received_data) 

        if self.received_data is None:
            # TODO LOGGING ERROR
            print("error")
            return None

        self.ack = self.communication.bytearray_to_dict(self.joints,self.received_data)
        print(self.ack)
        return self.ack

if __name__ == '__main__':
    x = ArtusAPI(target_ssid='ArtusMK6RH',communication_method=UART,port='/dev/ttyUSB0')
    x.start_connection()
    a = time.perf_counter()
    x.start_robot()
    time.sleep(0.001)
    n = 1000
    ns = 0
    ec = 0
    while ns < n:
        if not x.get_robot_states():
            print("ERROR")
            ec +=1
        else:
            print(x.joints['pinky_flex'].feedback_temperature)
        time.sleep(0.0014)
        ns+=1
    print("total time = "+str(time.perf_counter() - a))
    print("num error transmissions = "+str(ec))