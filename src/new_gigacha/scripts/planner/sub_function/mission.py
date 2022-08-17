from math import sqrt
from time import time, sleep
from math import cos, sin, pi, sqrt


class Mission():
    def __init__(self, sh, eg, pc, pl):
        self.perception = pc
        self.shared = sh
        self.ego = eg
        self.plan = pl
        self.parking = self.shared.park

        self.mission_complete = False
        self.timer = time()
        self.time_checker = False
        
        self.obstacle_checker = False
        self.stop_checker = False
        self.check = False
        self.prev_objx = 0

        self.now = 0
        self.parking_create = False
        self.parking_path_maker = False
        self.parking_forward_start = False
        self.parking_backward_start = False
        self.parking_switch = False

        self.selected = 0
        self.vote = {"345":0, "354":0, "435":0, "453":0, "534":0, "543":0}

        self.pickup_checker = False
        self.delivery_checker = False

    def go(self):
        self.ego.target_estop = 0x00
        self.ego.target_gear = 0
        self.ego.target_speed = 20.0
        self.plan.behavior_decision = "driving"
        
    def time_sleep(self, time):
        self.cur_t = time()
        while (time() - self.cur_t < time):
            pass
    
    def Parking2(self):
        if ((self.parking_create == False) and (20 <= self.ego.index <= 40)):
            self.plan.behavior_decision = "stop"
            self.ego.target_speed = 0
            self.ego.target_brake = 50
            sleep(3)
            self.parking.select_num = self.perception.parking_num
            self.ego.target_speed = 5
            self.ego.target_brake = 0
            self.parking_create = True
            self.plan.behavior_decision = "parking_trajectory_Create"
        if (self.parking_create and self.parking_switch == False):
            if (self.parking_forward_start == False and len(self.parking.forward_path.x) > 0):
                self.plan.behavior_decision = "parkingForwardOn"
                self.parking_forward_start = True
            if (35 <= int(self.parking.stop_index - self.parking.index) <= 55) and (self.parking.direction == 0):
                    self.ego.target_speed = 0
                    self.ego.target_brake = 50
                    sleep(3)
                    self.plan.behavior_decision = "parkingBackwardOn"
                    self.ego.target_gear = 2
                    self.ego.target_speed = 5
                    self.ego.target_brake = 0
            elif (15 <= int(self.parking.stop_index - self.parking.index) <= 25) and (self.parking.direction == 2):
                    self.ego.target_speed = 0
                    self.ego.target_brake = 50
                    sleep(3)
                    self.plan.behavior_decision = "driving"
                    self.parking.on = False
                    self.ego.target_gear = 0
                    self.ego.target_speed = 5
                    self.ego.target_brake = 0
                    self.parking_switch = True
    
    def Parking_Parallel(self):
        if ((self.parking_create == False) and (120 <= self.ego.index <= 140)):
            self.plan.behavior_decision = "stop"
            self.ego.target_speed = 0
            self.ego.target_brake = 50
            sleep(3)
            self.parking.select_num = self.perception.parking_num
            self.ego.target_speed = 5
            self.ego.target_brake = 0
            self.parking_create = True
            self.plan.behavior_decision = "parking_trajectory_Create"
        if (self.parking_create and self.parking_switch == False):
            if (self.parking_backward_start == False and len(self.parking.forward_path.x) > 0) and (self.parking.mindex + 20 <= self.ego.index <= self.parking.mindex + 40):
                self.ego.target_speed = 0
                self.ego.target_brake = 50
                sleep(3)
                self.plan.behavior_decision = "parkingBackwardOn"
                self.ego.target_gear = 2
                self.ego.target_speed = 5
                self.ego.target_brake = 0
                self.parking_backward_start = True
            if (15 <= int(self.parking.stop_index - self.parking.index) <= 25) and (self.parking.direction == 2):
                    self.ego.target_speed = 0
                    self.ego.target_brake = 50
                    sleep(3)
                    self.plan.behavior_decision = "parkingForwardOn"
                    self.ego.target_gear = 0
                    self.ego.target_speed = 5
                    self.ego.target_brake = 0
            elif (15 <= int(self.parking.stop_index - self.parking.index) <= 25) and (self.parking.direction == 0):
                    self.plan.behavior_decision = "driving"
                    self.parking.on = False
                    self.ego.target_gear = 0
                    self.ego.target_speed = 5
                    self.ego.target_brake = 0
                    self.parking_switch = True
    
    def Parking(self):
        if ((self.parking_create == False) and (910 <= self.ego.index <= 930)):
            self.plan.behavior_decision = "stop"
            self.ego.target_brake = 200 
            print("start")
            sleep(3)
            print("end")
            self.parking.select_num = self.perception.parking_num
            self.ego.target_brake = 0
            self.parking_create = True
            self.plan.behavior_decision = "parking_trajectory_Create"
        if self.parking_create:
            if (self.parking_forward_start == False) and (self.parking.mindex - 15 <= self.ego.index <= self.parking.mindex - 10):
                self.plan.behavior_decision = "parkingForwardOn"
                self.parking_forward_start = True
            elif (15 <= self.parking.stop_index - self.parking.index <= 18):
                    self.ego.target_estop = 1
                    if self.parking.direction == 0:
                        sleep(3)
                        self.plan.behavior_decision = "parkingBackwardOn"
                        self.ego.target_estop = 0
                        self.ego.target_brake = 0
                        self.ego.target_gear = 2
                        self.ego.target_speed = 5
                    elif self.parking.direction == 2:
                        sleep(3)
                        self.parking.on = False
                        self.ego.target_estop = 0
                        self.ego.target_brake = 0
                        self.ego.target_gear = 0
                        self.ego.target_speed = 5
                        self.plan.behavior_decision = "driving"

    def stop(self):
        self.sign_dis = sqrt(
            (self.perception.signx[0] - self.ego.x)**2 + (self.perception.signy[0] - self.ego.y)**2)
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
            for i in range(0, index):
                self.dis = sqrt(
                    (self.perception.objx[i] - self.ego.x)**2 + (self.perception.objy[i] - self.ego.y)**2)
                self.obs_dis = min(self.obs_dis, self.dis)
                print(len(self.perception.objx), " ", self.obs_dis)

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
            self.plan.behavior_decision = "driving"
            self.ego.target_brake = 0
            self.ego.target_speed = 10
        else:
            # if self.ego.index >= 410 and self.ego.index <= 470:
            if self.ego.index >= 600 and self.ego.index <= 650: # Siheung
                self.plan.behavior_decision = "stop"
                self.ego.target_brake = 50
                self.ego.target_speed = 0
            else:
                self.plan.behavior_decision = "driving"
                self.ego.target_brake = 0
                self.ego.target_speed = 10

    def turn_left(self):
        if self.perception.tleft == 1 :
            self.plan.behavior_decision = "driving"
            self.ego.target_brake = 0
            self.ego.target_speed = 10
        else:
            # if self.ego.index >= 410 and self.ego.index <= 470:
            if self.ego.index >= 3400 and self.ego.index <= 3475: # Siheung
                self.plan.behavior_decision = "stop"
                self.ego.target_brake = 50
                self.ego.target_speed = 0
            else:
                self.plan.behavior_decision = "driving"
                self.ego.target_brake = 0
                self.ego.target_speed = 10

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
            self.obs_dis = sqrt(
                (self.perception.objx[0] - self.ego.x)**2 + (self.perception.objy[0] - self.ego.y)**2)
            if self.obs_dis <= 10:
                if self.check == False:
                    self.plan.behavior_decision = "stop"
                    self.ego.target_brake = 33
                    self.wait_time = time()
                    self.check = True
                if self.plan.behavior_decision == "stop" and time() - self.wait_time > 5:
                    self.ego.target_brake = 0
                    self.ego.target_speed = 5.0
                    self.plan.behavior_decision = "static_obstacle_avoidance"
                    #self.sign_detected = 1
            elif self.obs_dis > 10:  # and self.sign_detected == 0:
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
                    objx.append(self.perception.tmp_objx[i] * cos(
                        theta) + self.perception.tmp_objy[i] * -sin(theta) + self.ego.x)
                    objy.append(self.perception.tmp_objx[i] * sin(
                        theta) + self.perception.tmp_objy[i] * cos(theta) + self.ego.y)
                self.prev_objx = self.perception.tmp_objx[0]
        self.perception.tmp_lidar_lock.release()
        self.perception.objx = objx
        self.perception.objy = objy

    def pickup(self):
        self.plan.behavior_decision = "delivery_mode"
        sign_dis = 0.0
        sign_dis = sqrt((self.perception.signx - self.ego.x)**2 + (self.perception.signy - self.ego.y)**2)
        # print("pickup : " , sign_dis)
        if 0 < sign_dis < 1.3 and self.pickup_checker == False:
            self.pickup_checker = True
            self.plan.behavior_decision = "stop"
            self.ego.target_brake = 200 
            sleep(5)
            self.ego.target_brake = 0
            self.plan.behavior_decision = "pickup_end"
            self.voting()
        elif 0 < sign_dis < 10:
            self.plan.behavior_decision = "pickup"
        if (self.pickup_checker == True):
            self.delivery()
        
    def delivery(self):
        self.plan.behavior_decision = "delivery"
        sign_dis = sqrt(
                (self.perception.B_x[self.selected] - self.ego.x)**2 + (self.perception.B_y[self.selected] - self.ego.y)**2)
        print("delivery : ", sign_dis)
        if(0 < sign_dis < 1.2 and self.delivery_checker == False):
            self.delivery_checker = True
            self.plan.behavior_decision = "stop"
            self.ego.target_brake = 200 
            sleep(5) 
            self.ego.target_brake = 0
        self.plan.behavior_decision = "delivery_end"

    def voting(self): 
        count = 0  
        while(count < 100):
            sort_result = ""
            sort_result += str(self.perception.first_sign) + str(self.perception.second_sign) + str(self.perception.third_sign)
            if (sort_result in self.vote.keys()):
                self.vote[sort_result] += 1
                count += 1
        print(self.vote)
        seq = max(self.vote, key=self.vote.get)
        seq_list = list(seq)
        for i in range(len(seq_list)):
            if int(seq_list[i]) == self.perception.target:
                self.selected = i
        print(self.selected)