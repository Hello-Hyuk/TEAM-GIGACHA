#!/usr/bin/env python3
import threading
from time import sleep

class MissionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan
               
    def run(self):
        while True:
            if self.shared.perception.signname == "turn_right_traffic_light":
                self.plan.state = "right_sign_detected"

            elif self.shared.perception.signname == "static_obstacle":
                self.plan.state = "static_obstacle_detected"           

            elif self.shared.perception.signname == "delivery":
                self.plan.state = "stop_sign_detected"

            elif self.shared.perception.signname == "child_area":
                self.plan.state = "child_area"
            
            elif self.shared.perception.signname == "turn_left_traffic_light":
                self.plan.state = "left_sign_detected"

            elif self.shared.perception.signname == "non_traffic_right":
                self.plan.state ="right_sign_area"

            else:
                self.plan.state = "go"

            # print(f"mission_planner : {self.state}")

            sleep(self.period)