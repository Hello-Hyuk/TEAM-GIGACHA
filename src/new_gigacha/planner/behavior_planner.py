#!/usr/bin/env python3
import threading
from time import sleep
from re import A
from math import sqrt
from std_msgs.msg import String
from planner_and_control.msg import Ego
from planner_and_control.msg import Perception
from planner_and_control.msg import Sign   #안쓰면 날리기
import mission

class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = Ego()
        self.perception = Perception()
        self.state = String()

        self.behavior = " "
        self.sign_dis = 100
        self.traffic_dis = 100
        self.go_side_check = False
        self.sign_detected = 0 # action just one time
        #self.mission = Mission(self.ego, self.perception)
        self.state_remember = "go"
    
    def run(self):
        while True:
            self.ego.speed = 1

            mission.update_parameter(self.ego, self.perception)

            if self.state_remember != self.state:
                self.state_remember = self.state
                mission.time_checker = False           

            if self.state == "parking":
                mission.parking()
                
            elif self.state == "static_obstacle_detected":
                mission.static_obstacle()
                
            elif self.state == "stop_sign_detected":
                mission.stop()

            elif self.state == "right_sign_detected":
                mission.turn_right()

            elif self.state == "left_sign_detected":
                mission.turn_left()
                
            elif self.state == "child_area":
                mission.child_area(self.perception.signx, self.perception.signy)

            elif self.state == "right_sign_area":
                mission.non_traffic_right()

            else:
                mission.go()

            print(f"behavior_planner : {mission.behavior_decision}")
            print(f"speed : {mission.ego.target_speed}")
            
            sleep(self.period)