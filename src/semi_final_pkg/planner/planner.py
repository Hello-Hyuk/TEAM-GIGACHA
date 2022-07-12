#!/usr/bin/env python3
import threading
from time import sleep
from std_msgs.msg import String

class Planner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan

        self.state = " "
        self.state_remember = "1st"
    
    def run(self):
        while True:
            try:
                self.mission.convert_lidar()
                # print("state : ", self.plan.state)

                if self.state_remember != self.plan.state:
                    self.state_remember = self.plan.state
                    self.mission.time_checker = False

                if self.plan.state == "parking":
                    self.mission.parking()

                else:
                    self.mission.go()

                # print(f"behavior_planner : {self.plan.behavior_decision}")
                # print(f"speed : {self.ego.target_speed}")
            except IndexError:
                # pass
                print("+++++++++++++++++")
            
            sleep(self.period)