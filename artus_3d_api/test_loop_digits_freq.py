import time
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir)
from Artus3DAPI import Artus3DAPI

artus3d = Artus3DAPI()

# start the connection to server
artus3d.start_connection()

time.sleep(1)

## name flex or digits
mon_nom = 'pinky_flex'
mon_cherche = '_flex'

# mon_nom = 'pinky_d2'
# mon_cherche = '_d'

max_ = 45


# start robot
artus3d.start_robot() # start twice because of bug
time.sleep(1)
artus3d.start_robot()
counter = 0
while True:
    # counter control
    if counter%40 == 0:
        counter+=1
        x = input('Ready to begin? (y/n)')
        if 'n' == x:
            artus3d.close_connection()
            quit()
    # increment counter
    if artus3d.joints[mon_nom].input_angle == 0:
        time.sleep(1)
        counter+=1
    elif artus3d.joints[mon_nom].input_angle == max_:
        time.sleep(1)

    # direction switch
    if artus3d.joints[mon_nom].input_angle <= 0:
        direction = 1
    elif artus3d.joints[mon_nom].input_angle >= max_:
        direction = 0

    # increment flex and _d1 _d2 values
    if direction:
        for joint_name,values in artus3d.joints.items():
            if joint_name == 'thumb_flex':
                continue
            elif mon_cherche in joint_name:
                values.input_angle+=5
    else:
        for joint_name,values in artus3d.joints.items():
            if joint_name == 'thumb_flex':
                continue
            elif mon_cherche in joint_name:
                values.input_angle-=5
    artus3d.send_target_command()
    time.sleep(0.1)