# Python Artus 3D Hand API
This repository contains the Python API for controlling the Artus 3D robotic hand.

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
├── test # a testing folder
```

## API Core
```python
class Artus3DAPI()
```
**parameters**:
- **communication_method**: UART or WiFi. Defaults to WiFi
- **port**: COM port for UART
- **target_ssid**: default is _Artus3DTester_ but replace with whatever your Artus 3D hand WiFi network name is. Only necessary for WiFi

**Class Methods**
- **`start_connection`**: start the connection to the Robot Hand over WiFi or UART as specified
- **`start_robot`**: send a start command to the Robot Hand over WiFi or UART as specified
- **`close_connection`**: close the connection to the Robot Hand over WiFi or UART as specified
- **`send_target_command`**: sends a targetting command based on the `input` data fields in the joints
- **`set_robot_params_by_joint_name`**: sets the joint input angle and input speed if not none by name
- **`set_robot_params_by_joint_index`**: sets the joint input angle and input speed if not none by index
- **`get_robot_states`**: send a message to the Robot Hand to receive joint data and populates `feedback` data fields in joints
- **`calibrate`**: send a calibrate command to the Robot Hand over WiFi or UART as specified
- **`sleep`**: send a sleep command to the Robot Hand over WiFi or UART as specified that saves the current positions of the hand to non-volatile memory in preparation for power cycling
- **`save_grasp_pattern`**: save a grasp pattern in robot_command to a text file in grasp_patterns folder
- **`get_grasp_pattern`**: get a grasp patptern from a text file in grasp_patterns folder

![Hand Joint Array Image Map](/public/Hand_Joint_Map.png)

## Joint Class
```python
class Artus3DJoint()
```
**parameters**:
- **joint_name**: name of the joint
- **maximum_angle_constraint and minimum_angle_constraint**: angle constraints
- **maximum_speed_constraint and minimum_speed_constraint**: speed constraints
- **input_speed**: input speed for next target
- **input_angle**: input angle for next target
- **feedback_angle**: reported angle
- **feedback_temperature**: reported temperature of actuator associated with the joint
- **feedback_current**: reported current of actuator associated with joint

**Class Methods**
- **`check_input_constraints`**: called automatically in `send_target_command`, this ensures that values written to the Robot Hand are in the format expected

## Updates and Revisions
It is possible to update the firmware on both the masterboard and actuator drivers. Actuator flashing can be made through the API, however improper flashing could corrupt the actuator drivers. This can by calling the `flash_file()` function when connected via WiFi. No hardware changes are required, the user only needs to provide a suitable binary path file for the driver released by Sarcomere Dynamics.

Masterboard updates can be done by putting the ESP into boot mode by shorting the _ESP Boot_ header pin with _GND_ and flashing over UART or USBC. 

![Boot Header Location](/public/Mainboard.png)