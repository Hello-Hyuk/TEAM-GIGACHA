#!/usr/bin/env python3
import threading
from time import sleep
import sys,os
from socket import MsgFlag
from .sub_function.find_local_path import findLocalPath
from .sub_function.LPP import path_maker  # LPP 구현 하기
from std_msgs.msg import String
from nav_msgs.msg import Path
from math import sqrt

class MotionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        #추가
        self.local_path = Path()
        self.trajectory = Path()
        self.generated_path = Path()
        self.trajectory_name = ""
        self.map_switch = 0

        self.current_lane = 0
        self.lane_weight = []
        self.isObstacle = [1000, 1000, 1000]

        self.current_lane = int(input("current lane(left : 1, right : 2) : "))

        if self.current_lane == 1:
            self.lane_weight = [10000, 0, 10000]
            self.trajectory.select_lane = 1
        else:
            self.lane_weight = [10000, 10000, 0]
            self.trajectory.select_lane = 2

    def weight_sign_function(self):
        for i in range(len(self.generated_path)):
            self.lane_weight[i] = sqrt((self.generated_path[i].poses[-1].pose.position.x - self.perception.signx[0])**2 + (self.generated_path[i].poses[-1].pose.position.y - self.perception.signy[0])**2)

    def select_trajectory(self):
        # if (len(self.local_path.poses) > 10):
        self.selected_lane = self.lane_weight.index(min(self.lane_weight))
        self.local_path = self.generated_path[self.selected_lane]
        self.trajectory_name = self.selected_lane

        tmp_trajectory = Path()
        for i in range (len(self.local_path.poses)):
            tmp_trajectory.x.append(self.local_path.poses[i].pose.position.x)
            tmp_trajectory.y.append(self.local_path.poses[i].pose.position.y)
        self.trajectory = tmp_trajectory
        
        print(f"lane_weight : {self.lane_weight}")
        if self.selected_lane == 1:
            print(f"motion_planner : global_path")
        else:
            print(f"motion_planner : selected lane {self.trajectory_name}, local_path")

    def weight_function_obstacle_avoidance(self):
        self.isObstacle = [1000, 1000, 1000]

        for i in range(len(self.generated_path)): # 0,1,2
            path_check = True
            if path_check == True:
                for j in range(len(self.generated_path[i].poses)): # paths' index
                    if path_check == False:
                        break
                    for k in range(len(self.perception.objx)): # of obj
                        ob_point_distance = sqrt((self.generated_path[i].poses[j].pose.position.x - self.perception.objx[k])**2 + (self.generated_path[i].poses[j].pose.position.y - self.perception.objy[k])**2)
                        if ob_point_distance < self.perception.objr[k]: #and self.Obstacle_in_section == 0:
                            self.isObstacle[i] = j
                            print("+++++++++obstacle in " + str(i) + "+++++++++++++++++")
                            #if(i == 1):
                            #    self.lane_weight[i] = 10000
                            #    self.lane_weight[i+1] = 0
                            # elif(i==2):
                            #     self.lane_weight[i] = 10000
                            #     self.lane_weight[i-1] = 0
                            path_check = False
                            break
                        # else:
                        #     self.isObstacle[i] = 1000
        print("isObstacle", self.isObstacle)
        
        if (self.selected_lane == 1 and self.isObstacle[1] != 1000):
            if(self.isObstacle[1] < self.isObstacle[2]):
                print("+++++++++++++\nobstacle in lane 1\n++++++++++++")
                self.lane_weight = [1000, 1000, 0]
        elif (self.selected_lane == 2 and self.isObstacle[2] != 1000):
            if(self.isObstacle[1] > self.isObstacle[2]):
                print("+++++++++++++\nobstacle in lane 2\n++++++++++++")
                self.lane_weight = [1000, 0, 1000]
        else:
            # self.ego.emergency_stop = 1
            pass

    def run(self):
        while True:
            self.local_path = findLocalPath(self.shared.global_path, self.shared.ego) # local path (50)
            self.generated_path = path_maker(self.local_path, self.shared.ego) # lattice paths

            if self.shared.plan.behavior_decision == "static_obstacle_avoidance":
                self.weight_function_obstacle_avoidance()
                self.select_trajectory()
            
            elif self.shared.plan.behavior_decision == "go_side":
                self.weight_sign_function()
                self.select_trajectory()
            
            elif self.shared.plan.behavior_decision == "stop":
                self.plan.trajectory.x = []
                self.plan.trajectory.y = []

            elif self.shared.plan.behavior_decision == "turn_right":
                self.lane_weight = [10000, 10000, 0]
                self.select_trajectory()

            elif self.shared.plan.behavior_decision == "turn_left":
                self.lane_weight = [10000, 0, 10000]
                self.select_trajectory()

            else:  ## self.shared.plan.behavior_decision == "go"
                self.select_trajectory()
            
            # path publish
            self.trajectory.select_lane = self.selected_lane
            self.global_path_pub.publish(self.global_path)
            self.trajectory_pub.publish(self.trajectory)
            # print(f"trajectory : {self.trajectory.x}")
            if len(self.generated_path) == 3:
                for i in range(1,4):
                    globals()['lattice_path_{}_pub'.format(i)].publish(self.generated_path[i-1])

            sleep(self.period)