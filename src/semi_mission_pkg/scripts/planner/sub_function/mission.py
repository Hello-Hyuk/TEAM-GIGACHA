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
        self.emergency_check = False
        self.obstacle_stop = False

        self.now = 0
        self.parking_create = False
        self.parking_path_maker = False
        self.parking_forward_start = False
        self.parking_backward_start = False
        self.parking_switch = False
        self.force_switch = False
        self.inflection_switch = False
        self.first_stop = False
        self.second_stop = False

        self.selected = 0
        self.vote = {"345":0, "354":0, "435":0, "453":0, "534":0, "543":0}

        self.pickup_checker = False
        self.delivery_checker = False
        
        self.uturn_stop = False
        self.speed = 10

    def range(self, a):
        return (a-30) <= self.ego.index <= a

    def target_control(self, brake, speed):
        self.ego.target_brake = brake
        self.ego.target_speed = speed

    def go(self):
        self.ego.target_estop = 0x00
        self.ego.target_gear = 0
        self.ego.target_speed = self.speed
        self.plan.behavior_decision = "driving"

    def Parking_stop_function(self, index1, index2):
        self.plan.behavior_decision = "driving"
        self.target_control(0, 5)
        if ((self.parking_create == False) and (index1 <= self.ego.index <= index2)):
            self.plan.behavior_decision = "stop"
            self.target_control(75, 0)
            sleep(3)
            self.parking.select_num = self.perception.parking_num
            self.target_control(0, 5)
            self.parking_create = True
            self.plan.behavior_decision = "parking_trajectory_Create"

    def Parking_Siheung_diagonal(self):
        if (self.parking_create == False):
            # if (20 <= self.ego.index <= 40) and self.first_stop == False: # Siheung
            if (910 <= self.ego.index <= 930) and self.first_stop == False: # K-City
                self.plan.behavior_decision = "stop"
                self.target_control(75, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.first_stop = True
            if self.first_stop == True and ((self.parking.select_num == 1) or (self.parking.select_num == 2) or (self.parking.select_num == 3)):
                self.target_control(0, 5)
                self.parking_create = True
                self.plan.behavior_decision = "parking_trajectory_Create"
            elif self.first_stop == True and self.parking.select_num == 4 or self.parking.select_num == 5 or self.parking.select_num == 6:
                # self.Parking_stop_function(115, 135) # Siheung
                self.Parking_stop_function(1025, 1045) # K-City

    def Parking_KCity_diagonal(self):
        if (self.parking_create == False):
            if (765 <= self.ego.index <= 795) and self.first_stop == False: # K-City
                self.plan.behavior_decision = "stop"
                self.target_control(75, 0)
                sleep(3)
                self.parking.select_num = self.perception.parking_num
                self.first_stop = True
            if self.first_stop == True and ((self.parking.select_num == 1) or (self.parking.select_num == 2) or (self.parking.select_num == 3)):
                self.target_control(0, 5)
                self.parking_create = True
                self.plan.behavior_decision = "parking_trajectory_Create"
            elif self.first_stop == True and self.parking.select_num == -1 or self.parking.select_num == 4 or self.parking.select_num == 5 or self.parking.select_num == 6:
                self.Parking_stop_function(875, 905) # K-City

        if (self.parking_create and self.parking_switch == False):
            if (self.parking_forward_start == False and len(self.parking.forward_path.x) > 0):
                self.parking.on = "on"
                self.plan.behavior_decision = "parkingForwardOn"
                self.parking_forward_start = True
            if (5 <= int(self.parking.stop_index - self.parking.index) <= 20) and (self.parking.direction == 0):
                    self.target_control(75, 0)
                    sleep(3)
                    self.plan.behavior_decision = "parkingBackwardOn"
                    self.ego.target_gear = 2
                    self.target_control(0, 5)
            elif (15 <= int(self.parking.stop_index - self.parking.index) <= 25) and (self.parking.direction == 2):
                    self.ego.target_speed = 0
                    self.ego.target_brake = 50
                    sleep(3)
                    self.plan.behavior_decision = "driving"
                    self.parking.on = "off"
                    self.ego.target_gear = 0
                    self.target_control(0, self.speed)
                    self.parking_switch = True

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

        if (2137 < self.ego.index < 2167) and self.obstacle_stop == False:
            self.target_control(75, 0)
            sleep(3)
            self.target_control(0, self.speed)
            self.obstacle_stop = True
        
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
                self.target_control(75, 0)
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
                self.target_control(75, 0)
            else:
                self.plan.behavior_decision = "driving"
                self.target_control(0, self.speed)

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

    def emergency_stop(self):
        self.ego.target_speed = 5
        self.plan.behavior_decision = "emergency_avoidance"
        if (self.shared.selected_lane == 0) and self.emergency_check == False:
            self.plan.behavior_decision = "stop"
            self.target_control(75, 0)
            sleep(5)
            self.target_control(0, 5)
            self.emergency_check = True

        elif (self.shared.selected_lane == 1) and self.emergency_check == True:
            self.emergency_check = False

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