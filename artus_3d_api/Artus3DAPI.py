"""
Artus 3D API created for the Artus 3D
Sarcomere Dynamics Inc.

"""

# imports
import time
import json
import logging

import os
import sys
from src.python_server import PythonServer
from src.python_uart import PythonEsp32Serial


class Artus3DAPI:
    def __init__(self,
                 communication_method = 'WiFi',
                 port='COM9',
                 target_ssid = 'Artus3DTester'
                 ):
        
        self.target_ssid = target_ssid
        self.communication_method = communication_method
        self.port = port

        # command codes
        self.target_cmd = '176'
        self.calibrate_cmd = '55'
        self.start_cmd = '88'
        self.getstates_cmd = '10'
        self.empty_message = "[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"

        # placeholders for values
        self.command = 0
        self.default_velocity = 90
        self.joint_names = ['thumb_flex','thumb_spread','thumb_d2','thumb_d1','index_flex','index_spread','index_d2',
                            'middle_flex','middle_spread','middle_d2','ring_flex','ring_spread','ring_d2','pinky_flex',
                            'pinky_spread','pinky_d2']
        
        # temporary dictionaries for constraints, joint parameters to be set and joint states to be read
        constraints = {
            'max':[90,30,90,90,90,15,90,90,15,90,90,15,90,90,15,90],
            'min':[0,-30,0,0,0,-15,0,0,-15,0,0,-15,0,0,-15,0]
        }
        joint_params = {
            'position': [0]*16,
            'velocity': [self.default_velocity]*16
        }
        joint_states = {
            'position': [0]*16,
            'temperature': [0]*16,
            'current': [0]*16
        }

        # create class variables
        self.constraints = self.joint_params = self.joint_states = None

        # create array for recursion
        populate = [self.constraints,self.joint_names,self.joint_params]
        info = [constraints,joint_params,joint_states]

        # populate array of dictionaries to be set to class variables
        for j in range(len(info)):
            # max and min constraints on angles
            populate[j] = {key:{k:v[i] for k,v in info[j].items()} for i,key in enumerate(self.joint_names)}

        # create dictionaries with the following structure
        # |
        # |->    joint_name
        #           |->     constraint (max,min)
        #           |->     joint params (position,velocity)
        #           |->     joint states (position,temperature,current)      
        self.constraints = populate[0]
        self.joint_params = populate[1]
        self.joint_states = populate[2]

        self.robot_command = self.grasp_pattern = None
        
        # instantiate server and serial classes
        self.python_server = PythonServer(reqReturnFlag = False,target_ssid=self.target_ssid)
        self.python_serial = PythonEsp32Serial(port=self.port)

    '''
    Getters for variables
    '''
    def get_constraints(self):
        return self.constraints
    
    def get_joint_params(self):
        return self.joint_params
    
    def get_joint_states(self):
        return self.joint_states

    '''
    Start the connection to the Robot Hand and send the Robot Hand a start command
    '''
    def start_connection(self):
        # start server in either wifi or UART mode
        if self.communication_method == "WiFi":
            try:
                self.python_server.start()
            except Exception as e:
                logging.error("error starting python server")
                print(e)
                pass

        if self.communication_method == "UART":
            try:
                self.python_serial.start()
                ## clear buffer
                for i in range(self.python_serial.esp32.in_waiting):
                    self.python_serial.receive()
            except Exception as e:
                logging.error("error starting serial connection")
                print(e)
                pass

        # send start command to the robot
        # set RTC values
        year = str(time.localtime().tm_year - 2000)
        month = str(time.localtime().tm_mon)
        day = str(time.localtime().tm_mday)
        hour = str(time.localtime().tm_hour)
        minute = str(time.localtime().tm_min)
        second = str(time.localtime().tm_sec)

        if int(month) < 10:
            month = '0'+ month
        if int(day) < 10:
            day = '0'+ day
        if int(hour) < 10:
            hour = '0'+ hour
        if int(minute) < 10:    
            minute = '0'+ minute
        if int(second) < 10:
            second = '0'+ second

        self.robot_command = "c88p[20,+"+year+",+"+month+",+"+day+",+"+hour+",+"+minute+",+"+second+",00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
        
        # send command
        self._send(self.robot_command)
        return self.robot_command
    
    '''
    Close the connection between the server and the Robot Hand
    '''
    def close_connection(self):
        try:
            # retrieve files either over WiFi or UART
            if self.communication_method == "WiFi": # wifi
                self.python_server.close()
                
            elif self.communication_method == "UART": # uart
                self.python_serial.close()
        except Exception as e:
            logging.warning("unable to close connection")

    '''
    Send a target command
    '''
    def send_target_command(self):
        self.command = self.target_cmd

        # look at constraints
        for key in ['max','min']:
            self._compare_constraints(self.constraints,self.joint_params,key)

        # change all values to integers
        for key,inner_dict in self.joint_params.items():
            for inner_key,inner_value in inner_dict.items():
                inner_value = int(inner_value)

        # set the command
        self.robot_command = 'c{0}p[{1}]v[{2}]end\n'.format(
            self.command,
            ','.join(str(inner_dict['position']) for inner_dict in self.joint_params.values()),
            ','.join(str(inner_dict['velocity']) for inner_dict in self.joint_params.values())
        )

        self._send(self.robot_command)
        return self.joint_params
    ''' 
    save grasp pattern from self.robot_command into separate text file
    '''
    def save_grasp_pattern(self,name=None):
        if name is None:
            name = input("Enter Grasp Pattern Name: ")
        filepath = os.path.join("grasp_patterns",name+'.txt')
        if not os.path.exists("grasp_patterns"):
            os.makedirs("grasp_patterns")

        if os.path.isfile(filepath):
            action = input("Rewrite last file? (y/n)\n")
            if action == 'y':
                with open(filepath,'w') as f:
                    f.write(self.robot_command)
            else: 
                print("File not overwritten..")

        return self.robot_command
    '''
    Load grasp pattern into self.robot_command from text file
    '''
    def get_grasp_pattern(self,name=None):
        if name is None:
            name = input("Enter Grasp Pattern Name: ")
        filepath = os.path.join("grasp_patterns",name+'.txt')

        if not os.path.isfile(filepath):
            print("File does not exist")

        else:
            with open(filepath,'r') as f:
                tmp_cmd = f.read()
                self.robot_command = tmp_cmd

        return self.robot_command
    '''
    Get states from Robot Hand
    '''
    def get_robot_states(self):

        self._send("c10p"+self.empty_message)

        str_return = ''
        while str_return == '':
            str_return = self._receive()

        # if empty Mk5+ compatible
        if "position" in str_return:
            return None,None
        
        valid_json_return = str_return.replace("'","\"")
        states_return = json.loads(valid_json_return)

        # return to form of self.joint_states
        new_joint_states = {key: {k:v[i] for k,v in states_return.items()} for i,key in enumerate(self.joint_names)}

        # update values in joint states dictionary
        self.update_joint_states(new_joint_states)

        return self.joint_states
    '''
    Update joint states such to be read out by users
    '''
    def update_joint_states(self,new_data:dict):
        self._update_dict(self.joint_states,new_data)
        return self.joint_states

    '''
    Reset specified actuator finger back to 0 chosen through parameter
    @param: joint - indice from joint map
    @param act - side of motor (dev)
    '''
    def locked_reset_low(self,joint:str,act:str):
        if int(joint) < 10:
            joint = '0'+joint
        self.robot_command = "c12p["+joint+",0"+act+",00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
        # send command
        self._send(self.robot_command)
        return self.robot_command

    '''
    Helper function to compare position to position hard min/max
    '''
    def _compare_constraints(self,constraint:dict,data:dict,constraint_key:str):
        for key,inner_dict in data.items():
            # replace mins
            if constraint_key == 'min' and inner_dict['position'] < constraint[key][constraint_key]:
                inner_dict['position'] = constraint[key][constraint_key]
            # replace maxs
            elif constraint_key == 'max' and inner_dict['position'] > constraint[key][constraint_key]:
                inner_dict['position'] = constraint[key][constraint_key]

        return data
    '''
    Update joint angles and velocity values in joint_params with matching keys of a dictionary given as a parameter
    @param: user joint angle/velocity dictionary with matching naming convention
    '''
    def update_joint_params(self,user_joint_dictionary:dict):
        self._update_dict(self.joint_params,user_joint_dictionary)
        return self.joint_params

    '''
    Recursive helper function to update dictionary values with matching keys
    '''
    def _update_dict(self,target, source):
        for key, value in source.items():
            if isinstance(value, dict) and key in target:
                self._update_dict(target[key], value)
            else:
                target[key] = value

    '''
    Send a target command to the Robot Hand
    '''
    def _send(self, message):
        try:
            # Send Command to Robot based on communication method
            if self.communication_method == "WiFi": # wifi
                message = self._check_command_string(message)
                print(message)
                # return
                self.python_server.send(message)
            elif self.communication_method == "UART": # uart
                self.python_serial.send(message)
        except Exception as e:
            logging.warning("unable to send command")
            print(e)
            pass
    
    '''
    Receive a message from the Robot Hand
    '''
    def _receive(self):
        """
        Recieve Command from Robot
        """
        try:    
            if self.communication_method == "WiFi": # wifi
                message  = self.python_server.receive()

            elif self.communication_method == "UART": # uart
                message  = self.python_serial.receive()
        except Exception as e:
            logging.warning("unable to receive message")
            print(e)

        return message

    '''
    Calibrate Robot Hand
    '''
    def calibrate(self):
        self.robot_command = self.calibrate_cmd+self.empty_message
        self._send(self.robot_command)

    '''
    Upload actuator driver bin file and flash
    '''
    def flash_file(self): # only WiFi is configured
        
        while True:
            num = input("Enter STM number (1-8) to flash or press enter to perform a full flash procedure: ")
            if num == '':
                self._send("c52p[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n")
                break
            elif int(num) > 0 and int(num) <= 8:
                self._send("c52p[+"+num+",00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n")
                break
            print("Invalid input. Please enter a number between 1 and 8 or press enter.")

        if self.communication_method == "WiFi": # wifi
            self.python_server.flash_wifi()
            
        elif self.communication_method == "UART": # uart
            self.python_serial.flash_serial()

    '''
    Helper function to check and parse the command string and make
        the values readable for the Robot Hand
    '''
    def _check_command_string(self, command_string):

        if "c176" in command_string:
            # print(command_string)
            # replace unnesserary 
            command_string = command_string.replace("\\n", "")
            command_string = command_string.replace("\n", "")
            command_string = command_string.replace("end", "")
            command_string = command_string.replace("c176", "")
            command_string = command_string.replace("p", "")
            command_string = command_string.replace("[", "")
            command_string = command_string.replace("]", "")

            #debugging
            # print(command_string)

            # seperate the two lists of joint angles and joint velocities
            command_string_position, command_string_velocity = command_string.split("v")
            # convert to list
            command_string_position = command_string_position.split(",")
            command_string_velocity = command_string_velocity.split(",")

            # debugging
            # print(command_string_velocity)

            # check the len of each element in the list
            for i in range(len(command_string_position)):
                if len(command_string_position[i]) == 1:
                    command_string_position[i] = "+0" + command_string_position[i]
                elif len(command_string_position[i]) == 2 and command_string_position[i][0] != "-":
                    command_string_position[i] = "+" + command_string_position[i]
                elif len(command_string_position[i]) == 2:
                    command_string_position[i] = "-0" + command_string_position[i][1:]

            for i in range(len(command_string_velocity)):
                if len(command_string_velocity[i]) == 1:
                    command_string_velocity[i] = "00" + command_string_velocity[i]
                elif len(command_string_velocity[i]) == 2:
                    command_string_velocity[i] = "0" + command_string_velocity[i]

            # convert back to original format
            command_string_position = "[" + ",".join(command_string_position) + "]"
            command_string_velocity = "[" + ",".join(command_string_velocity) + "]"

            # combine the two lists
            command_string = "c176p"+command_string_position + "v" + command_string_velocity + "end\n"

        return command_string
    
if __name__ == '__main__':
    test = Artus3DAPI()
    test.send_target_command()