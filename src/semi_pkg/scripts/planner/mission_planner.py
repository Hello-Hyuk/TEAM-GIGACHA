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
            try:                
                if self.shared.perception.signname == "parking":
                    self.plan.state = "parking"

                else:
                    self.plan.state = "go"

            except IndexError:
                print("++++++++mission_planner+++++++++")

            sleep(self.period)