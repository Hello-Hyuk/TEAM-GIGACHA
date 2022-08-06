import threading
import pymap3d
from time import sleep
from math import cos, sin, degrees, atan2, radians, pi, hypot

class LatController(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego

        self.global_path = parent.shared.global_path
 
        self.WB = 1.04 # wheel base
        self.k = 0.15 #1.5
        self.lookahead_default = 4 #look-ahead default

    def run(self):
        while True:
            try:
                if self.shared.state == "2nd":
                    self.path = self.global_path
                    # lookahead = min(self.k * self.ego.speed + self.lookahead_default, 6)
                    lookahead = 3
                    target_index = lookahead*10 + self.ego.index
                    
                    target_x, target_y = self.path.x[target_index], self.path.y[target_index]
                    print("target_x : ", target_x)
                    print("target_y : ", target_y)

                    tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360
                    
                    alpha = self.ego.heading - tmp
                    angle = atan2(2.0 * self.WB * sin(radians(alpha)) / lookahead, 1.0)

                    if degrees(angle) < 0.5 and degrees(angle) > -0.5:
                        angle = 0

                    self.ego.input_steer = max(min(degrees(angle), 27.0), -27.0)
                else:
                    target_x, target_y = self.ego.point_x, self.ego.point_y
                    
                    tmp = degrees(atan2(target_y, target_x)) % 360
                    distance = hypot(target_x, target_y)
                    alpha = -tmp
                    angle = atan2(2.0 * self.WB * sin(radians(alpha)) / distance, 1.0)

                    self.ego.input_steer = max(min(degrees(angle), 27.0), -27.0)

            except ZeroDivisionError:
                print("+++++++++++++++++")

            sleep(self.period)