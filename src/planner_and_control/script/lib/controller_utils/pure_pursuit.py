from math import hypot, cos, sin, degrees, atan2, radians, pi
import rospy

class PurePursuit:
    def __init__(self, eg, trajectory):
        self.ego = eg
        
        self.WB = 1.04 # wheel base
        self.k = 0.3 #1.5
        self.lookahead_default = 4 #look-ahead default
        self.path = trajectory

    def run(self):


        lookahead = min(self.k * self.ego.data.speed + self.lookahead_default, 6)
        # target_index = int(self.ego.data.index + lookahead*10)
        target_index = len(self.path.data.x)-1

        print(f"ego index : {self.ego.data.index}")
        print(f"target index : {target_index}")

        target_x, target_y = self.path.data.x[target_index], self.path.data.y[target_index]

        tmp = degrees(atan2(target_y - self.ego.data.y, target_x - self.ego.data.x)) % 360

        alpha = self.ego.data.heading - tmp
        angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)
    
        print("angle : ", degrees(angle)) 
        print(f"tmp : {tmp}")

        return max(min(degrees(angle), 27.0), -27.0)