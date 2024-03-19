
class ArtusCommunicator:
    def __init__(self):
        self.feedback_len = 81
        self.command_len = 34

    # abstract method
    def start(self):
        pass

    # abstract method
    def close(self):
        pass

    # abstract method
    def receive(self,data:list):
        pass

    # abstract method
    def send(self,data:bytearray):
        pass

    # create a byte array from joint dict
    def dict_to_bytearray(self,joint_dict:dict,command:int):

        # data to send
        send_data = bytearray(self.command_len)
        # append command first
        send_data[0] = command.to_bytes(1,byteorder='little')

        # fill the position data
        for name,joint_data in joint_dict.items():
            send_data[joint_data.joint_index + 1] = joint_data.input_angle.to_bytes(1,byteorder='little')
            send_data[joint_data.joint_index*2 + 1] = joint_data.input_speed.to_bytes(1,byteorder='little')

        # set last value to '\n'
        send_data[-1] = '\n'.encode('ascii')
        
        # return byte array to send
        return send_data
    
    # create a byte array from integer list
    def list_to_bytearray(self,command:int,values:list):

        # data to send
        send_data = bytearray(self.command_len)

        # append command first
        send_data[0:1] = command.to_bytes(1,byteorder='little')

        for i in range(len(values)):
            send_data[i+1:i+2] = values[i].to_bytes(1,byteorder='little')

        # set last value to '\n'
        send_data[-1:] = '\n'.encode('ascii')
        
        # return byte array to send
        return send_data


    # populate joint dict from byte data
    def bytearray_to_dict(self,joint_dict:dict,feedback:bytearray):
        
        data = []
        i = 0
        while i < 65:
            if 17 <= i <= 45:
                data.append(int.from_bytes(feedback[i:i+2],byteorder='big',signed=True))
                i+=2
            else:
                data.append(feedback[i].from_bytes(feedback[i:i+1],byteorder='little',signed=True))
                i+=1

        # populate feedback dictionary
        for name,joint_data in joint_dict.items():
            joint_data.feedback_angle = data[1+joint_data.joint_index]
            joint_data.feedback_current = data[1+16+joint_data.joint_index]
            joint_data.feedback_temperature = data[1+16+16+joint_data.joint_index]
            if joint_data.joint_index == 13:
                None

        # return acknowledge integer
        return data[0]


