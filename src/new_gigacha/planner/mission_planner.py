#!/usr/bin/env python3
import threading
from time import sleep
from std_msgs.msg import String
from planner_and_control.msg import Perception
from planner_and_control.msg import Ego
from planner_and_control.msg import Path
from planner_and_control.msg import Sign
from sensor_msgs.msg import PointCloud

class MissionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.state = ''
        self.obs_dis = 100
        self.sign = ''
        self.sign_dis = 100
    
    def run(self):
        while True:
            if self.shared.perception.signname == "turn_right_traffic_light":
                self.state = "right_sign_detected"

            elif self.shared.perception.signname == "static_obstacle":
                self.state = "static_obstacle_detected"           

            elif self.shared.perception.signname == "delivery":
                self.state = "stop_sign_detected"

            elif self.shared.perception.signname == "child_area":
                self.state = "child_area"
            
            elif self.shared.perception.signname == "turn_left_traffic_light":
                self.state = "left_sign_detected"

            elif self.shared.perception.signname == "non_traffic_right":
                self.state ="right_sign_area"

            else:
                self.state = "go"
             # print(f"mission_planner : {self.state}")

            sleep(self.period)