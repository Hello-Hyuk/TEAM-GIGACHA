
from lib.controller_utils.pid import PID

class longitudinalController:
    
    def __init__(self, ego):
        self.ego = ego
        #self.accel = PID(5, 0.5, 1)
        ##########for tuning
        self.accel = PID(10, 0.01, 0.1 , self.ego)
        ######################
        self.decel = PID(1, 1, 1, self.ego) #TODO ABS? instead of PID
        

    def run(self):
        if self.ego.target_speed == 0.0:
            return 0, self.decel.run() #speed, brake
        else:
            return self.accel.run(self.ego.speed, self.ego.target_speed), 0 #speed, brake