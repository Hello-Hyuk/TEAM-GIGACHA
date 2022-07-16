#!/usr/bin/env python3
import threading
from time import sleep
from std_msgs.msg import String
from math import pi, cos, sin

class Planner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan

        self.state_remember = "1st"

    def run(self):
        while True:
            try:
                theta = (self.ego.heading) * pi / 180

                self.ego.point_x = self.perception.objx[0] * cos(theta) + self.perception.objy[0] * -sin(theta) + self.ego.x
                self.ego.point_y = self.perception.objx[0] * sin(theta) + self.perception.objy[0] * cos(theta) + self.ego.y
                
                                
                # if  1:##처음상태:
                #     self.plan.state == "1st"


                #     ##맵을 다 땄다는 트리거==True


                # elif 2:##맵을 다 땄다는 트리거==True:
                #     self.plan.state =="after_2nd"
                    
            except IndexError:
                # pass
                print("+++++++++++++++++")
            
            sleep(self.period)