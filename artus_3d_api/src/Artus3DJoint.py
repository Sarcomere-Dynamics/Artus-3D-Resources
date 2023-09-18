
class Artus3DJoint:
    def __init__(self,joint_name,joint_index, maximum_angle, minimum_angle):
        self.joint_name = joint_name
        self.joint_index = joint_index
        self.maximum_angle_constraint = maximum_angle
        self.minimum_angle_constraint = minimum_angle
        self.maximum_speed_constraint = 100
        self.minimum_speed_constraint = 50

        self.input_angle = 0
        self.input_speed = 80
        self.feedback_angle = None
        self.feedback_temperature = None
        self.feedback_current = None

    def check_input_constraints(self):
        self.input_angle = int(self.input_angle)
        if self.input_angle > self.maximum_angle_constraint: 
            self.input_angle = self.maximum_angle_constraint
        elif self.input_angle < self.minimum_angle_constraint:
            self.input_angle = self.minimum_angle_constraint