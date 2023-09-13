# Python Artus 3D Hand API
This repository contains a Python API for controlling the Artus 3D robotic hand.

## Directory Structure
```bash
├── Artus3DAPI.py # Python API for Artus 3D
├── example.py # Example usage of the API
├── src # Dependencies for the API
│   ├── python_server.py # for WiFi communication
│   └── python_uart.py # for UART communication
├── grasps # grasps folder
```

## API Core
```python
class Artus3DAPI()
```

**parameters**:
- **communication_method**: UART or WiFi. Defaults to WiFi
- **port**: COM port for UART
- **target_ssid**: default is _Artus3DTester_ but replace with whatever your Artus 3D hand WiFi network name is. Only necessary for WiFi

**Class Attributes**:
- **joint_names**: array of our joint names in indexed order as sent to the Robot Hand. 
- **constraints**: inner dictionary of minimum and maximum positional constraints in a dictionary accessible by joint name. (e.g. `self.constraints['thumb_flex']['max']`)
- **joint_params**: inner dictionary of joint parameters (position and velocity) in a dictionary accessible by joint name. (e.g. `self.joint_parms['thumb_flex']['velocity']`)
- **joint_states**: inner dictionary of joint parameters (position, current and temperatures) in a dictionary accessible by joint name. (e.g. `self.joint_states['thumb_flex']['temperature']`)
- **robot_command**: robot command string to be sent to the Robot Hand

**Class Methods**
- **`start_connection`**: start the connection to the Robot Hand over WiFi or UART as specified
- **`close_connection`**: close the connection to the Robot Hand over WiFi or UART as specified
- **`send_target_command`**: set the robot_command and send the message to the Robot Hand
- **`save_grasp_pattern`**: save a grasp pattern in robot_command to a text file in grasp_patterns folder
- **`get_grasp_pattern`**: get a grasp patptern from a text file in grasp_patterns folder
- **`get_robot_states`**: send a message to the Robot Hand to receive joint data and populate the `joint_states` attribute
- **`update_joint_params`**: update `joint_params` attribute from a given dictionary with matching keys