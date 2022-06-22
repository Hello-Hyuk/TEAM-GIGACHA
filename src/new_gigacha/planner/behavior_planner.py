#!/usr/bin/env python3
import threading
from time import sleep
import mission

class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.state_remember = "go"
    
    def run(self):
        while True:

            mission.update_parameter(self.shared.ego, self.shared.perception, self.shared.behavior_decision)

            if self.state_remember != self.shared.state:
                self.state_remember = self.shared.state
                mission.time_checker = False           

            if self.shared.state == "parking":
                mission.parking()
                
            elif self.shared.state == "static_obstacle_detected":
                mission.static_obstacle()
                
            elif self.shared.state == "stop_sign_detected":
                mission.stop()

            elif self.shared.state == "right_sign_detected":
                mission.turn_right()

            elif self.shared.state == "left_sign_detected":
                mission.turn_left()
                
            elif self.shared.state == "child_area":
                mission.child_area(self.shared.perception.signx, self.shared.perception.signy)

            elif self.shared.state == "right_sign_area":
                mission.non_traffic_right()

            else:
                mission.go()

            print(f"behavior_planner : {mission.behavior_decision}")
            print(f"speed : {mission.ego.target_speed}")
            
            sleep(self.period)