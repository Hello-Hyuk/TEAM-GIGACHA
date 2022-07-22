from math import sqrt
from time import time
from math import cos, sin, pi, sqrt

class Mission():
    def __init__(self, sh, eg, pc, pl):
        self.perception = pc
        self.shared = sh
        self.ego = eg
        self.plan = pl
        
        self.timer = time()
        self.time_checker = False
        
        self.obstacle_checker = False
        self.stop_checker = False
        self.check = False
        self.prev_objx = 0

        self.traffic_checker = False

    def go(self):
        self.ego.target_estop = 0x00
        self.ego.target_gear = 0
        self.ego.target_speed = 10.0
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
                self.ego.target_speed = 10.0
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
        index = len(self.perception.objx)
        
        if (len(self.perception.objx) > 0):
            self.obs_dis = 15.5
            for i in range (0, index):
                self.dis = sqrt((self.perception.objx[i] - self.ego.x)**2 + (self.perception.objy[i] - self.ego.y)**2)
                self.obs_dis = min(self.obs_dis, self.dis)
            if self.obs_dis <= 15:
                self.ego.target_speed = 5.0
                self.obstacle_checker = True
                self.time_checker = False
                
        elif self.obstacle_checker == True:
            if self.time_checker == False:
                self.cur_t = time()
                self.time_checker = True
            if time() - self.cur_t < 5:
                self.ego.target_speed = 5.0
            else:
                self.ego.target_speed = 10.0


    def turn_right(self):
        if self.perception.tgreen == 1:
            self.plan.behavior_decision = "turn_right"
            self.ego.target_brake = 0
        else:
            if self.ego.index >= 410 and self.ego.index <= 470:
                self.plan.behavior_decision = "stop"
                self.ego.target_brake = 200
            else:
                self.plan.behavior_decision = "turn_right"
                self.ego.target_brake = 0

    
    def turn_left(self):
        self.plan.behavior_decision = "turn_left"
        if self.ego.index >= 400 and self.ego.index <= 470:
            print("case1")
            self.ego.target_speed = 0
            self.ego.target_brake = 200
            if self.perception.tleft == 1:
                self.traffic_checker = True
        if self.traffic_checker == True:
            print("case2")
            self.ego.target_speed = 10
            self.ego.target_brake = 0


    def non_traffic_right(self):
        if self.ego.index >= 430 and self.ego.index <= 450:
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
                 


    def child_area(self):
        if (len(self.perception.signx)!= 0):
            self.sign_dis = sqrt((self.perception.signx[0] - self.ego.x)**2 + (self.perception.signy[0] - self.ego.y)**2)
            if self.sign_dis <= 15:
                self.ego.target_speed = 7.0
            else:
                self.ego.target_speed = 10.0
            self.plan.behavior_decision = "child_area"

    def emergency_stop(self):
        if (len(self.perception.objx) > 0):
            self.obs_dis = sqrt((self.perception.objx[0] - self.ego.x)**2 + (self.perception.objy[0] - self.ego.y)**2)
            if self.obs_dis <= 10:
                if self.check == False:
                    self.plan.behavior_decision = "stop"
                    self.ego.target_brake = 200
                    self.wait_time = time()
                    self.check = True
                if self.plan.behavior_decision == "stop" and time() - self.wait_time > 5:
                    self.ego.target_brake = 0
                    self.ego.target_speed = 5.0
                    self.plan.behavior_decision = "static_obstacle_avoidance"
                    #self.sign_detected = 1
            elif self.obs_dis > 10: #and self.sign_detected == 0:
                self.plan.behavior_decision = "go"
                self.ego.target_speed = 10.0
                self.shared.selected_lane = 1
                self.check = False
        else:
            self.plan.behavior_decision = "go"

    def convert_lidar(self):
        theta = (self.ego.heading) * pi / 180
        size = 0
        objx = []
        objy = []
        self.perception.tmp_lidar_lock.acquire()
        size = len(self.perception.tmp_objx)
        if(size != 0):
            for i in range(size):
                objx.append(self.perception.tmp_objx[i] * cos(theta) + self.perception.tmp_objy[i] * -sin(theta) + self.ego.x)
                objy.append(self.perception.tmp_objx[i] * sin(theta) + self.perception.tmp_objy[i] * cos(theta) + self.ego.y)
    
        self.perception.lidar_lock.acquire()   
        self.perception.objy = []
        self.perception.objx = []
        self.perception.objx = objx
        self.perception.objy = objy
        self.perception.objw = self.perception.tmp_objw
        self.perception.objh = self.perception.tmp_objh
        self.perception.lidar_lock.release()
        self.perception.tmp_lidar_lock.release()
        

    def convert_lidar2(self):
        theta = (self.ego.heading) * pi / 180
        size = 0
        objx = []
        objy = []
        # self.perception.lidar_lock.acquire()   
        self.perception.objy = []
        self.perception.objx = []
        self.perception.tmp_lidar_lock.acquire()
        if len(self.perception.tmp_objx) != 0:
            if (self.prev_objx == self.perception.tmp_objx[0]):
                self.perception.tmp_objy = []
                self.perception.tmp_objx = []
                self.perception.objw = []
                self.perception.objh = []
            elif len(self.perception.tmp_objx) != 0:
                size = len(self.perception.tmp_objx)
                # size = len(self.perception.tmp_objx)//3
                for i in range(size):
                    objx.append(self.perception.tmp_objx[i] * cos(theta) + self.perception.tmp_objy[i] * -sin(theta) + self.ego.x)
                    objy.append(self.perception.tmp_objx[i] * sin(theta) + self.perception.tmp_objy[i] * cos(theta) + self.ego.y)
                self.prev_objx = self.perception.tmp_objx[0]
        self.perception.tmp_lidar_lock.release()
        self.perception.objx = objx
        self.perception.objy = objy
        # print("tmp :" ,len(self.shared.perception.tmp_objx))
        # print("real :" ,len(self.shared.perception.objx))
        # self.perception.lidar_lock.release()
     
  