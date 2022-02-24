from math import hypot, cos, sin, degrees, atan2, radians, pi
from planner_and_control.msg import Ego
import rospy

class PurePursuit:
    def __init__(self, eg, trajectory):
        self.ego = Ego()
        self.ego = eg
        
        self.WB = 1.04 # wheel base
        self.k = 0.3 #1.5
        self.lookahead_default = 4 #look-ahead default
        self.path = trajectory

    def run(self, ego):
        self.ego = ego
        lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6)

        # if self.ego.mode == "driving":
        #     lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6) # look-ahead
        # else :
        #     lookahead = 0.5
            
        target_index = int(self.ego.index + lookahead*10)
        print(self.ego.index)
        target_x = self.path.x[target_index]
        target_y = self.path.y[target_index]
        print(target_index)
        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360

        # if self.ego.mode == "backward" :
        #     self.ego.heading = (self.ego.heading + 180) % 360        
    
        alpha = self.ego.heading - tmp
        angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)
        #     lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6) # look-ahead
        # else :
        #     lookahead = 0.5
        
        print(f"heading : {self.ego.heading}")

        # if self.ego.mode == "backward" :
        #     angle = -angle

        return max(min(degrees(angle), 27.0), -27.0)