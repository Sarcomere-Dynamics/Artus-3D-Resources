![Sarcomere Dynamics Inc.](/public/SD_logo.png)
# Artus 3D Python API
This repository contains the Python API for controlling the Artus 3D Robotic Hand developed and maintained by Sarcomere Dynamics Inc. Please contact the team if there are any questions or issues that arise through the use of the API. 

## Table of Contents
* [Requirements](#requirements--install)
* [API Core](#api-core)
    * [Parameters](#parameters)
    * [Class Methods](#class-methods)
* [Joint Class](#joint-class)
    * [Parameters](#parameters-1)
    * [Class Variables](#class-variables)
    * [Class Methods](#class-methods-1)
    * [A note about joint limits](#a-note-about-joint-limits)
* [Running example.py](#running-examplepy)
* [Implementation Examples](#implementation-examples)
    * [Setting input values](#setting-input-values)
    * [Getting feedback values](#getting-feedback-values)
    * [Controlling multiple hands](#controlling-multiple-hands)
* [Teleoperation Considerations](#teleoperation-considerations)
* [Firmware Updates](#firmware-updates)
* [Revisions](#revisions)

## Requirements & Install
The API is a python based API developed and tested on `Python >= 3.10` please visit the [Python website](https://www.python.org/downloads/) to install Python.

To install the pip libraries, please run the following commands:\
`cd artus_3d_api`\
`pip install -r requirements.txt`

## API Core
```python
class Artus3DAPI()
```

### Parameters:
- **communication_method**: UART or WiFi.
- **port**: COM port for UART
- **target_ssid**: default will be set when shipped but replace with whatever your Artus 3D hand WiFi network name is. Only necessary for WiFi

Note that there should only be one single machine running one instance of the API to control 1-2 hands.

### Class Methods:
- **`start_connection`**: start the connection to the Artus 3D over WiFi or UART as specified
- **`start_robot`**: send a start command to the Artus 3D over WiFi or UART as specified
- **`close_connection`**: close the connection to the Artus 3D over WiFi or UART as specified
- **`send_target_command`**: sends a targetting command based on the `input` data fields in the joint dictionary
- **`get_robot_states`**: send a message to the Artus 3D to receive joint data and populates `feedback` data fields in joints
- **`calibrate`**: send a calibrate command to the Artus 3D over WiFi or UART as specified
- **`sleep`**: send a sleep command to the Artus 3D over WiFi or UART as specified that saves the current positions of the hand to non-volatile memory in preparation for power cycling
- **`save_grasp_pattern`**: save a grasp pattern in robot_command to a text file in grasp_patterns folder
- **`get_grasp_pattern`**: get a grasp patptern from a text file in grasp_patterns folder

## Joint Class
```python
class Artus3DJoint()
```
### Parameters:
- **`joint_name`**: name of the joint
- **`maximum_angle_constraint` and `minimum_angle_constraint`**: angle constraints
- **`maximum_speed_constraint` and `minimum_speed_constraint`**: speed constraints

### Class Variables:
- **`input_speed`**: input speed for next target
- **`input_angle`**: input angle for next target
- **`feedback_angle`**: reported angle
- **`feedback_temperature`**: reported temperature of actuator associated with the joint
- **`feedback_current`**: reported current of actuator associated with joint

### Class Methods:
- **`check_input_constraints`**: called automatically in `send_target_command`, this ensures that values written to the Artus 3D are in the format expected

![Hand Joint Array Image Map](/public/Hand_Joint_Map.png)

### A note about joint limits:
* All D2, D1 and flex joints have a range of 0-90 degrees
* Thumb spread is between -30 and 30, while the rest of the spreads are -15 to 15. 

## Running example.py
Before running the example script, determine whether your Artus 3D is running WiFi or UART, and edit the following line with the name of the target SSID for WiFi and port over UART
```python
artus3d = Artus3DAPI(target_ssid='Artus3DLH',port='/dev/ttyUSB0',communication_method='Wifi')
```
When running the example script, the following menu will be shown within the terminal:
```
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
Enter command:
```
The first thing to do is to start the connection to the hand by pressing "1". Next, you want to send the start robot command "2". Next to send a command, you can edit the `example_command.txt` file in the artus_3d_api/grasp_patterns folder. 

*To note when editing the grasps files:*\
`c176p[+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00]v[+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90]end`\
To edit the command there are a few things that need to be accounted for:
* each element in the array has 3 characters and must follow this convention
    * examples of allowable angles `+06` or `+90` or `-10` as these are all 3 characters long
    * velocities are in percentage, and should range from `+75` to `100` - note `100` does not have a +/- in front of it as it is already 3 characters in length
    * if this command convention is not followed, the hand may act unpredictably

## Implementation Examples
Below are some examples of how you can implement these functions in your code that are not covered by the `example.py` script.
### Setting input values:
*Name accessible :*
```python
artus3d.joints['thumb_flex'].input_angle = 45
```
*Through a Loop :*\
In this example, the assumption is you have an array of angles that are already mapped to the indices of the Artus 3D
```python
# input angles come from your control code, have 16 elements of type int or float and are mapped to our hand joint map
input_angles_from_control = []

for joint,joint_info in artus3d.joints.items():
    joint_info.input_angle = input_angles_from_control[joint_info.index]
```

### Getting feedback values:
In the same way as setting input values, we can access feedback data after calling `artus3d.get_robot_states()` by name.\
*Name accessible :*
```python
artus3d.joints['thumb_flex'].feedback_angle
```

### Controlling multiple hands:
We can define two instances of hands with different `port` and `target_ssid`. In theory, it can spin up an unlimited amount of hands, bottlenecked by the amount of wifi controllers and COM ports associated with the machine. e.g.
```python
artus3dLeft = Artus3DAPI(target_ssid='Artus3DLH',port='/dev/ttyUSB0',communication_method='UART')
artus3dRight = Artus3DAPI(target_ssid='Artus3DRH',port='/dev/ttyUSB1',communication_method='UART')
artusHands = [artus3dLeft,artus3dRight]
``` 

## Teleoperation Considerations
** **IT IS IMPORTANT TO ADD A DELAY BETWEEN SENDING MESSAGES, CURRENT SUGGESTED FREQUENCY FOR BEST USE IS 10 Hz OR DELAY OF 0.1s** **

## Firmware Updates
It is possible to update the firmware on both the masterboard and actuator drivers. Actuator flashing can be made through the API, however improper flashing could corrupt the actuator drivers. This can be done by calling the `flash_file()` function in the example script when connected via WiFi. No hardware changes are required, the user only needs to provide a suitable binary path file for the driver released by Sarcomere Dynamics.

Masterboard updates can be done by putting the ESP into boot mode by shorting the _ESP Boot_ header pin with _GND_ and flashing over UART or USBC.

![Boot Header Location](/public/Mainboard.png)

## Directory Structure
```bash
├── Artus3DAPI.py # Python API for Artus 3D
├── example.py # Example usage of the API
├── src # Dependencies for the API
│   ├── python_server.py # for WiFi communication
│   ├── python_uart.py # for UART communication
|   └── Artus3DJoint.py # our Joint class
├── grasp_patterns # grasps folder
├── requirements.txt # for easy pip install
```

## Revision Control
| Date  | Revision | Description | 
| :---: | :------: | :---------: |
| Nov. 14, 2023 | v1.0 | Initial release - Artus 3D Mk 5 |