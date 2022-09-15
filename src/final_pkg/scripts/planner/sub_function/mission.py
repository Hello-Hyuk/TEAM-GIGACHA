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

        self.time_checker = False
        
        self.obstacle_checker = False

        self.parking_create = False
        self.parking_backward_start = False
        self.parking_switch = False
        self.force_switch = False
        self.inflection_switch = False
        self.first_stop = False
        self.second_stop = False

        self.selected = 0
        self.vote = {"345":0, "354":0, "435":0, "453":0, "534":0, "543":0}

        self.signx = 0
        self.signy = 0
        self.B_x = [0,0,0]
        self.B_y = [0,0,0]

        self.pickup_checker = False
        self.delivery_checker = False
        self.voting_checker = False

        self.non_traffic_right_checker = 0
        self.uturn_stop = False

        self.speed = 15

    def range(self, a, b = 30):
        return (a-b) <= self.ego.index <= a

    def target_control(self, brake, speed):
        self.ego.target_brake = brake
        self.ego.target_speed = speed

    def go(self):
        if self.perception.tgreen == 1:
            self.plan.behavior_decision = "driving"
            self.target_control(0, self.speed)
        else:
            if self.range(1614) or self.range(2172) or self.range(3544) or self.range(6692) or self.range(6708) or self.range(8026) or self.range(8497):
                self.plan.behavior_decision = "stop"
                self.target_control(50,0)
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)
        
    def Parking_Siheung_Parallel(self):
        if (self.parking_create == False):
            if (75 <= self.ego.index <= 105) and self.first_stop == False:
                self.plan.behavior_decision = "stop"
                self.target_control(50, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.first_stop = True
                if self.parking.select_num == 1:
                    self.target_control(0, 5)
                    self.parking_create = True
                    self.plan.behavior_decision = "parking_trajectory_Create"
                else:
                    self.target_control(0, 5)
            elif self.first_stop == True and (265 <= self.ego.index <= 295) and self.second_stop == False:
                self.plan.behavior_decision = "stop"
                self.target_control(50, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.second_stop = True
                if self.parking.select_num == 2:
                    self.target_control(0, 5)
                    self.parking_create = True
                    self.plan.behavior_decision = "parking_trajectory_Create"
                else:
                    self.target_control(0, 5)
            elif self.second_stop == True and (465 <= self.ego.index <= 495):
                self.plan.behavior_decision = "stop"
                self.target_control(50, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.target_control(0, 5)
                self.parking_create = True
                self.plan.behavior_decision = "parking_trajectory_Create"

        if (self.parking_create and self.parking_switch == False):
            if (self.parking_backward_start == False and len(self.parking.forward_path.x) > 0) and (self.parking.mindex + 25 <= self.ego.index <= self.parking.mindex + 45):
                self.target_control(50, 0)
                sleep(3)
                self.plan.behavior_decision = "parkingBackwardOn"
                self.ego.target_gear = 2
                self.target_control(0, 5)
                self.parking.on = "on"
                self.parking_backward_start = True
            if (self.parking.direction == 2):
                if (1 <= self.parking.index <= 20) and self.force_switch == False:
                    self.target_control(70, 0)
                    # sleep(2)
                    self.target_control(0, 5)
                    self.force_switch = True
                    self.parking.on = "forced"
                    self.ego.target_steer = 27
                # elif (1 <= abs(int(self.parking.inflection_point - self.parking.index)) <= 10) and self.inflection_switch == False:
                elif (35 <= self.parking.index <= 50) and self.inflection_switch == False:
                    self.target_control(150, 0)
                    sleep(2)
                    self.inflection_switch = True
                    self.target_control(0, 5)
                    self.parking.on = "forced"
                    self.ego.target_steer = -27
                elif (10 <= int(self.parking.stop_index - self.parking.index) <= 20):
                    self.target_control(50, 0)
                    sleep(3)
                    self.plan.behavior_decision = "parkingForwardOn"
                    self.ego.target_gear = 0
                    self.target_control(0, 5)
                    self.parking.on = "forced"
                    self.ego.target_steer = -27
            # elif (1 <= abs(int(len(self.parking.forward_path.x) - self.parking.inflection_point - self.parking.index)) <= 5) and (self.parking.direction == 0):
            elif (30 <= self.parking.index <= 55) and (self.parking.direction == 0):
                    self.target_control(50, 0)
                    sleep(2)
                    self.plan.behavior_decision = "driving"
                    self.target_control(0, 5)
                    self.parking.on = "off"
                    self.parking_switch = True

    def Parking_KCity_Parallel(self):
        if (self.parking_create == False):
            if (9515 <= self.ego.index <= 9575) and self.first_stop == False:
                self.plan.behavior_decision = "stop"
                self.target_control(200, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.first_stop = True
                if (self.parking.select_num == 1) or (self.parking.select_num == 2):
                    self.target_control(0, 5)
                    self.parking_create = True
                    self.plan.behavior_decision = "parking_trajectory_Create"
                else:
                    self.target_control(0, 5)
            elif self.first_stop == True and (9685 <= self.ego.index <= 9745) and self.second_stop == False:
                self.plan.behavior_decision = "stop"
                self.target_control(200, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.second_stop = True
                if self.parking.select_num == 3:
                    self.target_control(0, 5)
                    self.parking_create = True
                    self.plan.behavior_decision = "parking_trajectory_Create"
                else:
                    self.target_control(0, 5)
            elif self.second_stop == True and (9885 <= self.ego.index <= 9945):
                self.plan.behavior_decision = "stop"
                self.target_control(200, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.target_control(0, 5)
                self.parking_create = True
                self.plan.behavior_decision = "parking_trajectory_Create"

        if (self.parking_create and self.parking_switch == False):
            if ((self.parking_backward_start == False) and len(self.parking.forward_path.x) > 0) and (self.parking.mindex + 15 <= self.ego.index <= self.parking.mindex + 30):
                self.target_control(200, 0)
                sleep(3)
                self.plan.behavior_decision = "parkingBackwardOn"
                self.parking.on = "on"
                self.ego.target_gear = 2
                self.target_control(0, 5)
                self.parking_backward_start = True
            if (self.parking.direction == 2):
                if (1 <= self.parking.index <= 20) and self.force_switch == False:
                    self.target_control(200, 0)
                    # sleep(2)
                    self.target_control(0, 5)
                    self.force_switch = True
                    self.parking.on = "forced"
                    self.ego.target_steer = 27
                # elif (1 <= abs(int(self.parking.inflection_point - self.parking.index)) <= 10) and self.inflection_switch == False:
                elif (35 <= self.parking.index <= 50) and self.inflection_switch == False:
                    self.target_control(200, 0)
                    sleep(2)
                    self.inflection_switch = True
                    self.target_control(0, 5)
                    self.parking.on = "forced"
                    self.ego.target_steer = -27
                elif (7 <= int(self.parking.stop_index - self.parking.index) <= 17):
                    self.target_control(200, 0)
                    sleep(3)
                    self.plan.behavior_decision = "parkingForwardOn"
                    self.ego.target_gear = 0
                    self.target_control(0, 5)
                    self.parking.on = "forced"
                    self.ego.target_steer = -27
            # elif (1 <= abs(int(len(self.parking.forward_path.x) - self.parking.inflection_point - self.parking.index)) <= 5) and (self.parking.direction == 0):
            elif (25 <= self.parking.index <= 40) and (self.parking.direction == 0):
                    self.parking.on = "off"
                    self.plan.behavior_decision = "driving"
                    self.target_control(0, self.speed)
                    self.parking_switch = True

    def u_turn(self):
        self.perception.tleft = 1
        if self.perception.tleft == 1 :
            self.plan.behavior_decision = "driving"
            if (5175 < self.ego.index < 5335):
                self.parking.on = "U_turn"
            if self.range(5365) and self.uturn_stop == False:
                    # self.plan.behavior_decision = "stop"
                    # self.target_control(75, 0)
                    # sleep(3)
                    self.plan.behavior_decision = "driving"
                    self.parking.on = "forced"
                    self.target_control(0, 5)
                    self.ego.target_steer = -27
                    self.uturn_stop = True
            elif self.ego.index > 5417 and self.uturn_stop == True:
                self.parking.on = "off"
        else:
            if self.range(5375):
                self.plan.behavior_decision = "stop"
                self.target_control(50, 0)
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)

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
                self.ego.target_speed = self.speed

    def turn_right(self):
        if self.perception.tgreen == 1:
            self.plan.behavior_decision = "driving"
            self.target_control(0, self.speed)
        else:
            # if self.ego.index >= 410 and self.ego.index <= 470:
            if self.ego.index >= 600 and self.ego.index <= 650: # Siheung
                self.plan.behavior_decision = "stop"
                self.target_control(50, 0)
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)

    def turn_left(self):
        if self.perception.tleft == 1 :
            self.plan.behavior_decision = "driving"
            self.target_control(0, self.speed)
        else:
            if self.range(4609):
                self.plan.behavior_decision = "stop"
                self.target_control(50, 0)
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)

    def non_traffic_right(self):
        if (self.range(5597, 20) and self.non_traffic_right_checker == 0) or (self.range(5831, 20) and self.non_traffic_right_checker == 1):
            self.plan.behavior_decision = "stop"
            self.target_control(50, 0)
            sleep(3)
            self.plan.behavior_decision = "driving"
            self.target_control(0, self.speed)
            self.non_traffic_right_checker += 1
            
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

    def convert_delivery(self):
        theta = (self.ego.heading) * pi / 180
        size = 0
        if(self.perception.signx != 0):
            self.signx = self.perception.signx[i] * cos(theta) + self.perception.signy[i] * -sin(theta) + self.ego.x
            self.signy = self.perception.signx[i] * sin(theta) + self.perception.signy[i] * cos(theta) + self.ego.y
        
        if(self.perception.first_sign != 0):
            for i in range(3):
                self.B_x[i] = self.perception.B_x[i] * cos(theta) + self.perception.B_y[i] * -sin(theta) + self.ego.x
                self.B_x[i] = self.perception.B_x[i] * sin(theta) + self.perception.B_y[i] * cos(theta) + self.ego.y

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

    def pickup(self):
        self.plan.behavior_decision = "pickup_mode"

        sign_dis = 0.0
        sign_dis = sqrt((self.signx - self.ego.x)**2 + (self.signy - self.ego.y)**2)

        if 0 < sign_dis < 10:
            self.plan.behavior_decision = "pickup"
        elif 0 < sign_dis < 1.3 and self.pickup_checker == False:
            self.pickup_checker = True
            self.plan.behavior_decision = "stop"
            self.target_control(200, 0)
            sleep(5)
            self.target_control(0, self.speed)
            self.plan.behavior_decision = "pickup_end"
        
    def delivery(self):
        self.plan.behavior_decision = "delivery_mode"

        if (self.perception.first_sign != 0) and self.voting_checker == False:
            self.voting()
            self.voting_checker = True
        
        sign_dis = 0.0
        sign_dis = sqrt((self.B_x[self.selected] - self.ego.x)**2 + (self.B_y[self.selected] - self.ego.y)**2)
     
        if 0 < sign_dis < 10:
            self.plan.behavior_decision = "delivery"
        if (0 < sign_dis < 1.2 and self.delivery_checker == False and self.voting_checker == True):
            self.delivery_checker = True
            self.plan.behavior_decision = "stop"
            self.target_control(200, 0)
            sleep(5) 
            self.target_control(0, self.speed)
            self.plan.behavior_decision = "delivery_end"

    # def pickup(self):
    #     self.plan.behavior_decision = "delivery_mode"
    #     sign_dis = 0.0
    #     sign_dis = sqrt((self.perception.signx - self.ego.x)**2 + (self.perception.signy - self.ego.y)**2)
    #     # print("pickup : " , sign_dis)
    #     if 0 < sign_dis < 1.3 and self.pickup_checker == False:
    #         self.pickup_checker = True
    #         self.plan.behavior_decision = "stop"
    #         self.target_control(200, 0)
    #         sleep(5)
    #         self.target_control(0, self.speed)
    #         self.plan.behavior_decision = "pickup_end"
    #         self.voting()
    #     elif 0 < sign_dis < 10:
    #         self.plan.behavior_decision = "pickup"
    #     if (self.pickup_checker == True):
    #         self.delivery()
        
    # def delivery(self):
    #     self.plan.behavior_decision = "delivery"
    #     sign_dis = sqrt((self.perception.B_x[self.selected] - self.ego.x)**2 + (self.perception.B_y[self.selected] - self.ego.y)**2)
    #     print("delivery : ", sign_dis)
    #     if(0 < sign_dis < 1.2 and self.delivery_checker == False):
    #         self.delivery_checker = True
    #         self.plan.behavior_decision = "stop"
    #         self.target_control(200, 0)
    #         sleep(5) 
    #         self.target_control(0, self.speed)
    #     self.plan.behavior_decision = "delivery_end"