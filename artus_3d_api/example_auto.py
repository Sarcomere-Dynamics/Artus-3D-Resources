
import time

import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI

def auto_example():
    hand_robot_api = Artus3DAPI()

    time.sleep(2)

    input("ready to start demo?")

    while True:
    # start
    # hand_robot_api.start()

        # wait
        time.sleep(1)

        # move commands
        with open('joint_commands_auto.txt',"r") as f:
            line = "start"
            while line:
                if line == "\n": 
                    time.sleep(5)
                    print("waiting...")
                line = f.readline()
                hand_robot_api.send(line)
                time.sleep(10)

        # time.sleep(5)
        # input("end demo")
        

if __name__ == '__main__':
    auto_example()
