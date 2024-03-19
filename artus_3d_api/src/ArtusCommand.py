class ArtusCommand:
    def __init__(self,index=None,angle=None,speed=None):
        self.input_angle = angle
        self.input_speed = speed
        self.joint_index = index