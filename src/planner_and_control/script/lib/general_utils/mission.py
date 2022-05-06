import rospy
import time

class Mission:
    def __init__(self, eg, behav):
        self.ego = eg
        self.behavior = behav

    def driving(self):
        self.ego.gear = 0
        self.ego.target_speed = 20
        self.behavior.decision = "driving"

    def parking(self):
        if self.ego.index >= 500 and self.ego.index <= 550:
            self.ego.brake = 1
            self.ego.target_speed = 0
            self.behavior.decision = "parking_ready"
            time.sleep(5)

            self.ego.brake = -1
            self.ego.target_speed = 5
            self.behavior.decision = "parking_start"
            
            if self.ego.index >= 700 and self.ego.index <= 750:
                self.ego.brake = 1
                self.ego.target_speed = 0
                self.ego.gear = 2
                self.behavior.decision = "parking_complete"
                time.sleep(5)
                
        if self.behavior.decision == "parking_complete":
            self.ego.brake = -1
            self.ego.target_speed = 5
            self.behavior.decision = "backward driving"

            if (self.ego.index >= 500 and self.ego.index <= 550) and self.behavior.decision == "backward driving":
                self.ego.brake = 1
                self.ego.target_speed = 0
                self.ego.gear = 0
                self.behavior.decision = "go back to driving"
                time.sleep(5)

                self.ego.brake = -1
                self.ego.target_speed = 15
                self.behavior.decision = "driving"

                    