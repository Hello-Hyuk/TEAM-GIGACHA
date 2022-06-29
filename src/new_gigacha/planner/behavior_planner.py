#!/usr/bin/env python3
import threading
from time import sleep
from re import A
from math import sqrt
from std_msgs.msg import String
from sub_function import Mission

class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan

        self.sign_dis = 100
        self.traffic_dis = 100
        self.go_side_check = False
        self.sign_detected = 0 # action just one time
        self.mission = Mission(self.ego, self.perception, self.plan)
        self.state_remember = "go"
    
    def run(self):
        while True:
            self.ego.speed = 1

            self.mission.update_parameter(self.ego, self.perception, self.plan)

            if self.state_remember != self.state:
                self.state_remember = self.state
                self.mission.time_checker = False           

            if self.state == "parking":
                self.mission.parking()
                
            elif self.state == "static_obstacle_detected":
                self.mission.static_obstacle()
                
            elif self.state == "stop_sign_detected":
                self.mission.stop()

            elif self.state == "right_sign_detected":
                self.mission.turn_right()

            elif self.state == "left_sign_detected":
                self.mission.turn_left()
                
            elif self.state == "child_area":
                self.mission.child_area(self.perception.signx, self.perception.signy)

            elif self.state == "right_sign_area":
                self.mission.non_traffic_right()

            else:
                self.mission.go()

            print(f"behavior_planner : {self.shared.behavior_decision}")
            print(f"speed : {self.ego.target_speed}")
            
            sleep(self.period)