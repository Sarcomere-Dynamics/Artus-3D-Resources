import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI,UART,WIFI

def main_menu():
    return input('''
Artus 3D API v1.0.0
Command options:
1. start connection to hand
2. start robot
3. calibrate
4. send command from grasp_patterns/example_command.txt
5. save grasp pattern to file
6. use grasp pattern from file
7. get robot states
8. ~ reset finger ~
9. open hand from grasp_patterns/grasp_open.txt
10. close hand using grasp in grasp_patterns/grasp.txt
11. firmware flash actuators
12. save current hand state for power cycle
13. close connection
Enter command: ''')

LHB = 'Artus3DTesterLHBLACK'
LHW = 'Artus3DTesterLHWHITE'
LHW = 'Artus3DTesterLHWHITE'
RHW = 'Artus3DTesterRHWHITE'

def example():
    artus3d = Artus3DAPI(target_ssid=LHB,port='/dev/ttyUSB0',communication_method=UART)
    while True:
        user_input = main_menu()
        match user_input:
            case "1":
                artus3d.start_connection()
            case "2":
                artus3d.start_robot()
            case "3":
                artus3d.calibrate()
            case "4":
                with open(os.path.join("grasp_patterns","example_command.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "5":
                artus3d.save_grasp_pattern()
            case "6":
                artus3d.get_grasp_pattern()
            case "7":
                artus3d.get_robot_states()
            case "8": 
                joint = input('choose joint angle 0-16: ')
                user_act = input("choose actuator:\n0:both\n1:act1\n2:act2")
                artus3d.locked_reset_low(joint,user_act)
            case "9":
                with open(os.path.join("grasp_patterns","grasp_open.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "10":
                with open(os.path.join("grasp_patterns","grasp.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.robot_command = command
                    artus3d.send_target_command()
            case "11":
                artus3d.flash_file() 
            case "12":
                artus3d.sleep()
            case "13":
                artus3d.close_connection()       

if __name__ == '__main__':
    example()


