import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI
import keyboard

# import grasps
graspClose = current_directory+"\\grasp_patterns\\grasp_close.txt"
graspOpen  = current_directory+"\\grasp_patterns\\grasp_open.txt"

# fill dict
grasps = {
    "open":graspOpen,
    "close":graspClose
}

# wait time
# delay for UART
delay = 0.01
# no delay for WIFI


def example_control_loop():
    hand_robot_api = Artus3DAPI()

    time.sleep(1)

    # create command dict
    command_dict = {key: None for key in grasps}

    # load grasps
    for key in grasps:
        with open(grasps[key],'r') as f:
            command_dict[key] = f.read()
    
    # start the hand
    hand_robot_api.start()
    
    time.sleep(5)

    hand_robot_api.command = 176
    hand_robot_api.joint_angles = [00,00,00,00,20,00,00,00,20,00,00,00,00,00,00,00]
    hand_robot_api.robot_command = hand_robot_api.parse_command()
    print(hand_robot_api.robot_command)

    hand_robot_api.send(hand_robot_api.robot_command)

    time.sleep(1)

example_control_loop()