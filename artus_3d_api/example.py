import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI

def main_menu():
    return input(
        '''
Artus 3D API 1.0
Command options:
1. start
2. calibrate
3. send command from grasp_patterns/example_command.txt
4. save grasp pattern to file
5. use grasp pattern from file
6. get robot states
7. ~ reset finger ~
8. open hand from grasp_patterns/grasp_open.txt
9. close hand using grasp in grasp_patterns/grasp.txt
10. firmware flash actuators
Enter command: 
'''
    )

def example():
    artus3d = Artus3DAPI()
    while True:
        user_input = main_menu()
        match user_input:
            case 1:
                artus3d.start_connection()
            case 2:
                artus3d.calibrate()
            case 3:
                with open(os.path.join("grasp_patterns","example_command.txt"), "r") as f:
                    command = f.read()
                artus3d.send_target_command(command)
            case 4:
                artus3d.save_grasp_pattern()
            case 5:
                artus3d.get_grasp_pattern()
            case 6:
                artus3d.get_robot_states()
            case 7: 
                joint = input('choose joint angle 0-16: ')
                user_act = input("choose actuator:\n0:both\n1:act1\n2:act2")
                artus3d.locked_reset_low(joint,user_act)
            case 8:
                with open(os.path.join("grasp_patterns","grasp_open.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send(command)
            case 9:
                with open(os.path.join("grasp_patterns","grasp.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send(command)
            case 10:
                artus3d.flash_file()        

if __name__ == '__main__':
    example()


