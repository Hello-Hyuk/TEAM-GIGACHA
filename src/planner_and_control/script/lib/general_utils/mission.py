import rospy
from math import sqrt
import time

class Mission():
    def __init__(self, eg, pc):
        self.perception = pc
        self.ego = eg
        self.mission_complete = False

    def go(self):
        self.ego.gear = 0
        self.ego.target_speed = 20
        self.ego.behavior_decision = "driving"
        
    def parking(self):
        if self.ego.index >= 500 and self.ego.index <= 550:
            self.ego.brake = 1
            self.ego.target_speed = 0
            self.ego.behavior_decision = "parking_ready"
            time.sleep(5)

            self.ego.brake = -1
            self.ego.target_speed = 5
            self.ego.behavior_decision = "parking_start"
            
            if self.ego.index >= 700 and self.ego.index <= 750:
                self.ego.brake = 1
                self.ego.target_speed = 0
                self.ego.gear = 2
                self.ego.behavior_decision = "parking_complete"
                time.sleep(5)
                
        if self.behavior.decision == "parking_complete":
            self.ego.brake = -1
            self.ego.target_speed = 5
            self.ego.behavior_decision = "backward_driving"

            if (self.ego.index >= 500 and self.ego.index <= 550) and self.behavior.decision == "backward driving":
                self.ego.brake = 1
                self.ego.target_speed = 0
                self.ego.gear = 0
                self.ego.behavior_decision = "go_back_to_driving"
                time.sleep(5)

                self.ego.brake = -1
                self.ego.target_speed = 15
                self.ego.behavior_decision = "driving"

    def stop(self):
        self.sign_dis = sqrt((self.perception.signx[0] - self.ego.x)**2 + (self.perception.signy[0] - self.ego.y)**2)
        if self.sign_dis <= 5:
            if self.go_side_check == False:
                self.ego.behavior_decision = "stop"
                self.wait_time = time()
                self.go_side_check = True
            if self.ego.behavior_decision == "stop" and time() - self.wait_time > 3:
                self.ego.behavior_decision = "go"
                self.sign_detected = 1
        elif self.sign_dis > 5 and self.sign_detected == 0:
            self.ego.behavior_decision = "go_side"
            self.go_side_check = False

    def static_obstacle(self, objx, objy):
        if (len(self.perception.objx)!= 0):
            self.obs_dis = sqrt((self.perception.objx[0] - self.ego.x)**2 + (self.perception.objy[0] - self.ego.y)**2)
            if self.obs_dis <= 3:
                self.ego.target_speed = 5.0
            else:
                self.ego.target_speed = 10.0
            self.ego.behavior_decision = "static_obstacle_avoidance"


    def turn_right(self):
        if self.perception.tgreen == 1:
            self.ego.behavior_decision = "turn_right"
        else:
            if self.ego.index >= 1000 and self.ego.index <= 1050:
                self.ego.behavior_decision = "stop"
            else:
                self.ego.behavior_decision = "turn_right"
    
    def turn_left(self):  #left 수정
        if self.perception.tgreen == 1:
            self.ego.behavior_decision = "turn_right"
        else:
            if self.ego.index >= 1000 and self.ego.index <= 1050:
                self.ego.behavior_decision = "stop"
            else:
                self.ego.behavior_decision = "turn_right"

    def child_area(self):
        pass