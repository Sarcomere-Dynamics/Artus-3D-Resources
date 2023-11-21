import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI,UART,WIFI

MK5LH = 'ArtusMk5LH'
sleep = 0.35
artus = Artus3DAPI(target_ssid=MK5LH,communication_method=WIFI)

artus.start_connection()
time.sleep(1)
input("start?")
artus.start_robot()
time.sleep(sleep)

for joint,joint_stuff in artus.joints.items():
    joint_stuff.input_speed = 99


artus.joints['thumb_flex'].input_angle = 80
artus.send_target_command()
time.sleep(sleep)
artus.joints['index_flex'].input_angle = 90
artus.send_target_command()
time.sleep(sleep)
artus.joints['pinky_flex'].input_angle = 90
artus.send_target_command()
time.sleep(sleep)
artus.joints['ring_flex'].input_angle = 90
artus.send_target_command()
time.sleep(sleep)
artus.joints['middle_flex'].input_angle = 90
artus.send_target_command()
time.sleep(sleep)
artus.joints['ring_flex'].input_angle = 90
artus.send_target_command()
time.sleep(1)
artus.joints['thumb_d1'].input_angle = 60
artus.send_target_command()
time.sleep(sleep)
artus.joints['thumb_d2'].input_angle = 60
artus.send_target_command()
time.sleep(sleep)
artus.joints['middle_d2'].input_angle = 60
artus.send_target_command()
time.sleep(sleep)
artus.joints['pinky_d2'].input_angle = 60
artus.send_target_command()
time.sleep(sleep)
artus.joints['index_d2'].input_angle = 60
artus.send_target_command()
time.sleep(sleep)

input("open")

artus.joints['thumb_flex'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['index_flex'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['pinky_flex'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['ring_flex'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['middle_flex'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['ring_flex'].input_angle = 00
artus.send_target_command()
time.sleep(1)
artus.joints['thumb_d1'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['thumb_d2'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['middle_d2'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['pinky_d2'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)
artus.joints['index_d2'].input_angle = 00
artus.send_target_command()
time.sleep(sleep)