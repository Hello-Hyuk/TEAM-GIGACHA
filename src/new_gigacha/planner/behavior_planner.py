#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.mission import Mission
from std_msgs.msg import String

class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.state = String()

        self.behavior = " "
        self.sign_dis = 100
        self.traffic_dis = 100
        self.go_side_check = False
        self.sign_detected = 0 # action just one time
        self.mission = Mission(self.ego, self.perception, self.shared.plan)
        self.state_remember = "go"
    
    def run(self):
        while True:
            # self.mission.update_parameter(self.ego, self.perception, self.shared.plan)

            if self.state_remember != self.shared.state:
                self.state_remember = self.shared.state
                self.mission.time_checker = False           

            if self.shared.state == "parking":
                self.mission.parking()
                
            elif self.shared.state == "static_obstacle_detected":
                self.mission.static_obstacle()
                
            elif self.shared.state == "stop_sign_detected":
                self.mission.stop()

            elif self.shared.state == "right_sign_detected":
                self.mission.turn_right()

            elif self.shared.state == "left_sign_detected":
                self.mission.turn_left()
                
            elif self.shared.state == "child_area":
                self.mission.child_area(self.shared.perception.signx, self.shared.perception.signy)

            elif self.shared.state == "right_sign_area":
                self.mission.non_traffic_right()

            else:
                self.mission.go()

            print(f"behavior_planner : {self.shared.plan.behavior_decision}")
            print(f"speed : {self.ego.target_speed}")
            
            sleep(self.period)