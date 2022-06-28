from planner_and_control.msg import Local

class Ego():
    def __init__(self, parent):
        #Local to Ego
        self.x = 0
        self.y = 0
        self.dr_x = 0
        self.dr_y = 0
        self.heading = 0
        self.index = 0

        #Serial to Ego
        self.speed = 0
        self.brake = 0
        self.gear = 0
        self.steer = 0
        self.alive = 0

        #Planner to Controller
        self.target_speed = 0
        self.target_gear = 0

        #Controller to Serial
        self.input_estop = 1
        self.input_gear = 1
        self.input_speed = 0
        self.input_steer = 0
        self.input_brake = 0