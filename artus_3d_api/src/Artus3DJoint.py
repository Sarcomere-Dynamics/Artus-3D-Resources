import logging 

class Artus3DJoint:
    def __init__(self,joint_name=None,joint_index=None, maximum_angle=None, minimum_angle=None):
        self.joint_name = joint_name
        self.joint_index = joint_index
        self.maximum_angle_constraint = maximum_angle
        self.minimum_angle_constraint = minimum_angle
        self.maximum_speed_constraint = 100
        self.minimum_speed_constraint = 60

        self.input_angle = 0
        self.input_speed = 80
        self.feedback_angle = None
        self.feedback_temperature = None
        self.feedback_current = None

    def check_input_constraints(self):
        self.input_angle = int(self.input_angle)
        self.input_speed = int(self.input_speed)
        if self.input_angle > self.maximum_angle_constraint: 
            self.input_angle = self.maximum_angle_constraint
            # logging.info(f"{self.joint_name} input angle exceeds max limit - changed to {self.maximum_angle_constraint}")
        elif self.input_angle < self.minimum_angle_constraint:
            self.input_angle = self.minimum_angle_constraint
            # logging.info(f"{self.joint_name} input angle exceeds min limit - changed to {self.minimum_angle_constraint}")

        if self.input_speed > self.maximum_speed_constraint:
            self.input_speed = self.maximum_speed_constraint
            # logging.info(f"{self.joint_name} input speed exceeds max limit - changed to {self.maximum_speed_constraint}")
        elif self.input_speed < self.minimum_speed_constraint:
            self.input_speed = self.minimum_speed_constraint
            # logging.info(f"{self.joint_name} input speed exceeds min limit - changed to {self.minimum_speed_constraint}")