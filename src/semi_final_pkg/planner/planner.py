#!/usr/bin/env python3
import threading
from math import hypot
from time import sleep
from std_msgs.msg import String
from math import pi, cos, sin

class Planner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.global_path = self.shared.global_path

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.state = self.shared.state


    def run(self):
        while True:
            try:

                theta = (self.ego.heading) * pi / 180

                if self.state == "2nd":

                    min_dis = -1
                    min_idx = 0
                    step_size = 100
                    save_idx = self.ego.index

                    for i in range(max(self.ego.index - step_size, 0), self.ego.index + step_size):
                        try:
                            dis = hypot(self.global_path.x[i] - self.ego.x, self.global_path.y[i] - self.ego.y)
                        except IndexError:
                            break
                        if (min_dis > dis or min_dis == -1) and save_idx <= i:
                            min_dis = dis
                            min_idx = i
                            save_idx = i

                    self.ego.index = min_idx   
                    print("index : ",self.ego.index)          
                
                else:
                    self.ego.point_x = self.perception.objx
                    self.ego.point_y = self.perception.objy

   
                                        
                            
            except IndexError:
                # pass
                print("+++++++++++++++++")
            
            sleep(self.period)