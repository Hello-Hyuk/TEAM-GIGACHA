#!/usr/bin/env python3
import threading
from time import sleep

class MissionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
    
        self.ego = parent.shared.ego
        self.perception = parent.shared.perception
        self.state = parent.shared.plan.state
    
    def run(self):
        while True:

            if self.perception.signname == "turn_right_traffic_light":
                self.state = "right_sign_detected"

            elif self.perception.signname == "static_obstacle":
                self.state = "static_obstacle_detected"           

            elif self.perception.signname == "delivery":
                self.state = "stop_sign_detected"

            elif self.perception.signname == "child_area":
                self.state = "child_area"
            
            elif self.perception.signname == "turn_left_traffic_light":
                self.state = "left_sign_detected"

            elif self.perception.signname == "non_traffic_right":
                self.state ="right_sign_area"

            else:
                self.state = "go"
    
            sleep(self.period)