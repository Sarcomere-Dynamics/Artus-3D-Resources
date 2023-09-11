# Artus 3D Hand API

API for controlling the Artus 3D dexterous robotic hand.


## Directory Structure
```bash
├── artus_3d_api.py # Python API for Artus 3D
├── example.py # Example usage of the API
├── joint_control_command.txt # Example joint control command
├── src # Dependencies for the API
│   ├── python_server.py # for WiFi communication
│   └── python_uart.py # for UART communication
```

## example.py procedure
1. Power on the Artus 3D
2. Connect to the Artus3DMkX wifi network and enter password
3. run the example.py python script
4. when prompted, enter "1" to start the hand and wait a couple seconds
5. If the hand _NEEDS_ to be calibrated, enter "2"
6. wait for the hand to finish calibrating all of it's joints before entering a new command
7. modify the joint_control_command.txt file with desired joint position (0-90) degrees and joint speed (0-100) percent
8. press "3" to move the fingers to their respective joint positions

## API Core

### Artus3DAPI


```python
class Artus3DAPI()
```
Provides an API for controlling the Artus 3D dexterous robotic hand.

**Parameters**:
- **communication_method**: Communication method to use. Can be either 'WiFi' or 'UART'. Defaults to 'WiFi'.
- **PORT**: If 'UART' is chosen, then specify port
- **TARGET_SSID**: need to copy name of Artus 3D Wifi network here

**Methods**:
- **`start()`**: Initalize the hand.
- **`set_joint_dictionary(key:str,joint_angle:int,joint_speed:int)`**: set the joint angle and joint speed of a single joint.
- **`set_joint_angles_dictionary(joint_angles_dict: dict)`**: Copy a joint dictionary with matching keys to the class joint dictionary for use. Auto fills velocities to default velocities if missing
    - **"joint_control_command" structure**: "c176p"+joint_positions_list_str+"v"+joint_velocities_list_str+"end\n"
- **`set_robot_command_from_dictionary()`**: set the robot command from the joint dictionary
- **`set_joint_angles()`**: set joint angles if known joint map index
- **`set_joint_velocities()`**: set joint velocities if known joint map index
- **`set_command()`**: set command code
- **`set_robot_command()`**: set robot command message to send to hand
- **`get_robot_states()`**: Gets the robot states from the hand.
- **`get_debug_message()`**: Gets the debug message from the hand.
- **`save_grasp_pattern(name: str)`**: Saves the current joint configuration as a grasp pattern (joint control command).
- **`get_grasp_pattern(name: str)`**: Returns the joint control command of a saved grasp pattern.
- **`get_robot_states()`**: Gets the robot states from the hand. 
    - **"robot_states_str" structure**: "a{x}p"+joint_positions_list_str+"t"+joint_temperatures_list_str+"c"+joint_currents_list_str+"end\n"
    - **"robot_states_" structure**: {
        'positions' : [position array (deg)],
        'temperatures' : [temperature array (C)]
        'currents' : [current array (mA)]
    }
- **`save_grasp_pattern(name: str)`**: Save the robot states from the hand.
- **`calibrate()`**: Calibrate the hand.
- **`flash_file()`**: flash stms.
- **`close()`**: close the connection to the hand.


## Joint Array Map
numbered from thumb to pinky, base to tip.
![hand joint array image](/public/Hand_Joint_Map.png)

## Procedure
1. Power on the hand.
2. Connect to the ESP32 WiFi network on your computer.
3. Use the API to send commands to the hand.

## Example Usage
```python
from artus_3d_api import Artus3DAPI

hand_api = Artus3DAPI()

# 1. Always calibrate on startup
hand_api.calibrate()

# 2. Send Joint Control Command (wait for the calibration to complete)
## format the command
#### joint array format:
# [thumbflex, thumbabduct, thumbd2, thumbd1, 
# indexflex, indexabduct, indexd2, 
# middleflex, middleabduct, middled2, 
# ringflex, ringabduct, ringd2, 
# pinkyflex, pinkyabduct, pinkyd2]
#### Range of motion:  (abduction range --> -35 to 35 (thumb), -20 to 20 (other fingers) || all other angles --> 0 to 90)
#### Velocity: 50 to 100
joint_positions = "[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]" # 16 joint positions (in degrees)
joint_velocities = "[70,70,70,70,70,70,70,100,70,70,70,70,70,70,70,70]" # 16 joint velocities
joint_control_command = "c176p"+joint_positions+"v"+joint_velocities+"end\n"
hand_api.send(joint_control_command) # send the command to the hand

# 3. save and use grasp patterns
## save grasp pattern
open_grasp_pattern = "c176p[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]v[70,70,70,70,70,70,70,100,70,70,70,70,70,70,70,70]end\n"
hand_api.save_grasp_pattern(name='open', grasp_pattern=open_grasp_pattern)
## use grasp pattern
grab_pattern = hand_api.get_grasp_pattern(name="open")
## send the command to the hand
hand_api.send(grasp_pattern)

# 4. get robot states
## get positional and force data from the hand
### 1st array is joint angles 
### 2nd array is current draw

```




