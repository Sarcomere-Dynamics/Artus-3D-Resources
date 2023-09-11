import time

import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI


def example():

    # array holder
    grasps = []

    # imports the artus_3d_api
    hand_robot_api = Artus3DAPI()

    time.sleep(2)

    # start the hand
    hand_robot_api.start()

    # save commands to array
    with open("test_joints.txt","r") as f:
        grasps.append(f.readline()) # open
        grasps.append(f.readline()) # closed

    hand_robot_api.send(grasps[0])

    # main loop
    i=0
    j=0
    while True:
        hand_robot_api.send(grasps[i])
        print(grasps[i])

        # delay
        time.sleep(6)

        # increment counter or reset if out of range
        i+=1
        j+=1
        
        if i > 1:
            i=0

        # wait for input 
        input("continue?")


if __name__ == '__main__':
    # main()
    example()
