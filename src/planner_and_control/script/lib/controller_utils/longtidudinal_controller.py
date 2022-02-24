from lib.controller_utils.pid import PID
from planner_and_control.msg import Ego

class longitudinalController:
    
    def __init__(self, eg, target_speed):
        self.ego = Ego()
        self.ego = eg
        self.target_speed = target_speed
        #self.accel = PID(5, 0.5, 1)
        ##########for tuning
        self.accel = PID(10, 0.01, 0.1 , self.ego)
        ######################
        self.decel = PID(1, 1, 1, self.ego) #TODO ABS? instead of PID
        

    def run(self):
        if self.target_speed == 0.0:
            return 0, self.decel.run() #speed, brake
        else:
            return self.accel.run(self.ego.speed, self.target_speed), 0 #speed, brake