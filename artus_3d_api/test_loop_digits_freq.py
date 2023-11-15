import time
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir)
from Artus3DAPI import Artus3DAPI

LHB = 'Artus3DTesterLHBLACK'
LHW = 'Artus3DTesterLHWHITE'
RHW = 'Artus3DTesterRHWHITE'
W = 'WiFi'
U = 'UART'


artus3dleft = Artus3DAPI(target_ssid=RHW,communication_method=U,port='/dev/ttyUSB0')
artus3dright = Artus3DAPI(target_ssid=LHB,port='/dev/ttyUSB0',communication_method='UART')

# start the connection to server
artus3dleft.start_connection()
# artus3dright.start_connection()

time.sleep(1)

## name flex or digits
mon_nom = 'index_flex'
mon_cherche = '_spread'

# mon_nom = 'pinky_d2'
# mon_cherche = '_d'
123
max_ = 28
step_ = 8


# start robot
artus3dleft.start_robot() # start twice because of bug
# artus3dright.start_robot()
time.sleep(1)
# artus3dright.start_robot()
counter = 0

while True:
    # counter control
    if counter%10 == 0:
        counter+=1
        x = input('Ready to begin? (y/n)')
        if 'n' == x:
            for joint_name,values in artus3dright.joints.items():
                artus3dleft.joints[joint_name].input_angle = 0
                artus3dleft.joints[joint_name].input_speed = 96
                artus3dright.joints[joint_name].input_angle = 0
                artus3dright.joints[joint_name].input_speed = 96
            artus3dleft.send_target_command()
            artus3dleft.close_connection()
            # time.sleep(0.001)
            # artus3dright.send_target_command()
            # artus3dright.close_connection()
            quit()
    # increment counter
    if artus3dleft.joints[mon_nom].input_angle == 0:
        time.sleep(2)
        counter+=1
    elif artus3dleft.joints[mon_nom].input_angle >= max_:
        time.sleep(2)
        None

    # direction switch
    if artus3dleft.joints[mon_nom].input_angle <= 0:
        direction = 1
    elif artus3dleft.joints[mon_nom].input_angle >= max_:
        direction = 0

    # increment flex and _d1 _d2 values
    if direction:
        for joint_name,values in artus3dleft.joints.items():
            if 'thumb_' in joint_name or 'index_' in joint_name or 'middle_' in joint_name or 'pinky_' in joint_name:
                if 'spread' in joint_name: 
                    continue
                artus3dleft.joints[joint_name].input_angle+=step_
                artus3dleft.joints[joint_name].input_speed = 86
                artus3dright.joints[joint_name].input_speed = 86
                artus3dright.joints[joint_name].input_angle+=step_
            else:
                continue
                artus3dleft.joints[joint_name].input_angle+=step_
                artus3dright.joints[joint_name].input_speed = 80
                artus3dright.joints[joint_name].input_angle+=step_
    else:
        for joint_name,values in artus3dleft.joints.items():
            if 'thumb_' in joint_name or 'index_' in joint_name or 'middle_' in joint_name or 'pinky_' in joint_name:
                if 'spread' in joint_name: 
                    continue
                artus3dleft.joints[joint_name].input_angle-=step_
                artus3dleft.joints[joint_name].input_speed = 86
                artus3dright.joints[joint_name].input_speed = 86
                artus3dright.joints[joint_name].input_angle-=step_
            else :
                continue
                artus3dleft.joints[joint_name].input_angle-=step_
                artus3dright.joints[joint_name].input_speed = 80
                artus3dright.joints[joint_name].input_angle-=step_
                
    artus3dleft.send_target_command()
    # time.sleep(0.001)
    # artus3dright.send_target_command()
    # artus3dright.get_robot_states()
    time.sleep(0.15)