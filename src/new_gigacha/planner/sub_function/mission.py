from math import sqrt
from time import time

class Mission():
    def __init__(self, eg, pc, pl):
        self.perception = pc
        self.ego = eg
        self.plan = pl
        self.mission_complete = False
        self.timer = time()
        self.time_checker = False
        self.obstacle_checker = False
        self.stop_checker = False
        self.check = False

    def update_parameter(self, eg, pc, pl):
        self.perception = pc
        self.ego = eg
        self.plan.behavior_decision = pl.plan.behavior_decision

    def go(self):
        self.ego.gear = 0
        self.ego.target_speed = 20.0
        self.plan.behavior_decision = "driving"
        
    def parking(self):
        if self.ego.index >= 500 and self.ego.index <= 550:
            self.ego.brake = 1
            self.ego.target_speed = 0.0
            self.plan.behavior_decision = "parking_ready"
            time.sleep(5)

            self.ego.brake = -1
            self.ego.target_speed = 5
            self.plan.behavior_decision = "parking_start"
            
            if self.ego.index >= 700 and self.ego.index <= 750:
                self.ego.brake = 1
                self.ego.target_speed = 0.0
                self.ego.gear = 2
                self.plan.behavior_decision = "parking_complete"
                time.sleep(5)
                
        if self.behavior.decision == "parking_complete":
            self.ego.brake = -1
            self.ego.target_speed = 5.0
            self.plan.behavior_decision = "backward_driving"

            if (self.ego.index >= 500 and self.ego.index <= 550) and self.behavior.decision == "backward driving":
                self.ego.brake = 1
                self.ego.target_speed = 0.0
                self.ego.gear = 0
                self.plan.behavior_decision = "go_back_to_driving"
                time.sleep(5)

                self.ego.brake = -1
                self.ego.target_speed = 15.0
                self.plan.behavior_decision = "driving"

    def stop(self):
        self.sign_dis = sqrt((self.perception.signx[0] - self.ego.x)**2 + (self.perception.signy[0] - self.ego.y)**2)
        if self.sign_dis <= 5:
            if self.go_side_check == False:
                self.plan.behavior_decision = "stop"
                self.wait_time = time()
                self.go_side_check = True
            if self.plan.behavior_decision == "stop" and time() - self.wait_time > 3:
                self.plan.behavior_decision = "go"
                self.sign_detected = 1
        elif self.sign_dis > 5 and self.sign_detected == 0:
            self.plan.behavior_decision = "go_side"
            self.go_side_check = False

    def static_obstacle(self):
        self.plan.behavior_decision = "static_obstacle_avoidance"
        if (len(self.perception.objx) > 0):
            index = len(self.perception.objy)
            self.obs_dis = 15.5
            for i in range (0, index):
                self.dis = sqrt((self.perception.objx[i] - self.ego.x)**2 + (self.perception.objy[i] - self.ego.y)**2)
                self.obs_dis = min(self.obs_dis, self.dis)
            if self.obs_dis <= 15:
                self.ego.target_speed = 5.0
                self.obstacle_checker = True
                self.time_checker = False
            elif self.obs_dis > 15 and self.obstacle_checker == True:
                if self.time_checker == False:
                    self.cur_t = time()
                    self.time_checker = True

                if time() - self.cur_t < 3:
                    self.ego.target_speed = 5.0
                else:
                    self.ego.target_speed = 15.0
            else:
                self.ego.target_speed = 15.0

    def turn_right(self):
        if self.perception.tgreen == 1:
            self.plan.behavior_decision = "turn_right"
            self.ego.target_brake = 0
        else:
            if self.ego.index >= 1000 and self.ego.index <= 1050:
                self.plan.behavior_decision = "stop"
                self.ego.target_brake = 200
            else:
                self.plan.behavior_decision = "turn_right"
                self.ego.target_brake = 0

    
    def turn_left(self):
        if self.perception.tleft == 1:
            self.plan.behavior_decision = "turn_left"
            self.ego.target_brake = 0
        else:
            if self.ego.index >= 2750 and self.ego.index <= 2800:
                self.plan.behavior_decision = "stop"
                self.ego.target_brake = 200
            else:
                self.plan.behavior_decision = "turn_left"
                self.ego.target_brake = 0


    def non_traffic_right(self):
        if self.ego.index >= 1000 and self.ego.index <= 1050:
            self.plan.behavior_decision = "stop"
            if self.time_checker == False:
                self.time_checker = True
                self.cur_t = time()
            
            if time() - self.cur_t > 3:
                self.plan.behavior_decision = "turn_right"
        else:
            self.plan.behavior_decision = "turn_right"

        # if(len(self.perception.rightx)!=0):
        #     self.right_dis=sqrt((self.perception.rightx[0] - self.ego.x)**2 + (self.perception.righty[0] - self.ego.y)**2)
        #     if self.right_dis<=5:
        #         if self.go_check == False:
        #             self.plan.behavior_decision = "stop"
        #             self.wait_time_right=time()
        #             self.go_check = True
        #         if self.plan.behavior_decision =="stop" and time()-self.wait_time_right>2:
        #             self.plan.behavior_decision = "turn_right"
                 


    def child_area(self, signx, signy):
        if (len(self.perception.signx)!= 0):
            self.sign_dis = sqrt((self.perception.signx[0] - self.ego.x)**2 + (self.perception.signy[0] - self.ego.y)**2)
            if self.sign_dis <= 15:
                self.ego.target_speed = 7.0
            else:
                self.ego.target_speed = 20.0
            self.plan.behavior_decision = "child_area"

    def emergency_stop(self):
        if (len(self.perception.objx) > 0):
            self.obs_dis = sqrt((self.perception.objx[0] - self.ego.x)**2 + (self.perception.objy[0] - self.ego.y)**2)
            if self.obs_dis <= 5:
                print("!!!!!!!!!!!!Obstacle Detected!!!!!!!!!!!!")
                if self.check == False:
                    self.plan.behavior_decision = "stop"
                    self.ego.target_brake = 200
                    self.wait_time = time()
                    self.check = True
                if self.plan.behavior_decision == "stop" and time() - self.wait_time > 5:
                    self.plan.behavior_decision = "static_obstacle_detected"
                    #self.sign_detected = 1
            elif self.obs_dis > 5: #and self.sign_detected == 0:
                self.plan.behavior_decision = "go"
                self.check = False
        else:
            self.plan.behavior_decision = "go"
            