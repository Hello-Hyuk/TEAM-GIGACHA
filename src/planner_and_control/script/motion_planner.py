#!/usr/bin/env python3
import sys,os
from socket import MsgFlag
import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.general_utils.read_global_path import read_global_path
from lib.planner_utils.find_local_path import findLocalPath
from lib.planner_utils.LPP import path_maker
from planner_and_control.msg import Path as CustomPath
from planner_and_control.msg import Ego
from planner_and_control.msg import Perception
from std_msgs.msg import String
from nav_msgs.msg import Path
from math import sqrt

class Motion_Planner:
    def __init__(self):
        rospy.init_node('Motion_Planner', anonymous = False)

        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/perception', Perception, self.perception_callback)
        rospy.Subscriber('/behavior', String, self.behavior_callback)

        # rviz
        self.global_path_pub = rospy.Publisher('/global_path', CustomPath, queue_size = 1)
        self.trajectory_pub = rospy.Publisher('/trajectory', CustomPath, queue_size = 1)
        for i in range(1,4):
            globals()['lattice_path_{}_pub'.format(i)] = rospy.Publisher('lattice_path_{}'.format(i),Path,queue_size=1) 

        self.ego = Ego()
        self.perception = Perception()
        self.behavior = ''
        self.global_path = CustomPath()
        self.trajectory = CustomPath()
        self.generated_path = Path()
        self.trajectory_name = ""

        self.path_name = 'songdo_track'
        self.global_path = read_global_path(self.path_name)

        self.current_lane = 0
        self.lane_weight = []

        self.current_lane = input("current lane(left : 1, right : 2) : ") # temporary code(to aviod lidar dectection)

        if self.current_lane == '1':
            self.lane_weight = [10000, 0, 10000]
            
        else:
            self.lane_weight = [10000, 10000, 0]

    def ego_callback(self, msg):
        self.ego = msg

    def perception_callback(self, msg):
        self.perception = msg
    
    def behavior_callback(self, msg):
        self.behavior = msg.data

    # avoidance driving
    def weight_function_obstacle_avoidance(self):
        for i in range(len(self.generated_path)): # 0,1,2
            path_check = True
            if path_check == True:
                for j in range(len(self.generated_path[i].poses)): # paths' index
                    if path_check == False:
                        break
                    for k in range(len(self.perception.objx)): # # of obj
                        ob_point_distance = sqrt((self.generated_path[i].poses[j].pose.position.x - self.perception.objx[k])**2 + (self.generated_path[i].poses[j].pose.position.y - self.perception.objy[k])**2)
                        if ob_point_distance < self.perception.objr[k]:
                            self.lane_weight[i] = 10000
                            path_check = False
                            break

    # go_to_sign
    def weight_sign_function(self):
        for i in range(len(self.generated_path)):
            self.lane_weight[i] = sqrt((self.generated_path[i].poses[-1].pose.position.x - self.perception.signx[0])**2 + (self.generated_path[i].poses[-1].pose.position.y - self.perception.signy[0])**2)

    def select_trajectory(self):
        self.selected_lane = self.lane_weight.index(min(self.lane_weight))
        self.local_path = self.generated_path[self.selected_lane]
        self.trajectory_name = self.selected_lane

        tmp_trajectory = CustomPath()
        for i in range (len(self.local_path.poses)):
            tmp_trajectory.x.append(self.local_path.poses[i].pose.position.x)
            tmp_trajectory.y.append(self.local_path.poses[i].pose.position.y)
        self.trajectory = tmp_trajectory
        
        print(f"lane_weight : {self.lane_weight}")
        if self.selected_lane == 1:
            print(f"motion_planner : global_path")
        else:
            print(f"motion_planner : selected lane {self.trajectory_name}, local_path")

    def run(self):
        self.local_path = findLocalPath(self.global_path, self.ego) # local path (50)
        self.generated_path = path_maker(self.local_path, self.ego) # lattice paths

        if self.behavior == "go":
            self.select_trajectory()
        
        if self.behavior == "obstacle avoidance":
            self.weight_function_obstacle_avoidance()
            self.select_trajectory()
        
        if self.behavior == "go_side":
            self.weight_sign_function()
            self.select_trajectory()
        
        if self.behavior == "stop":
            self.trajectory.x = []
            self.trajectory.y = []

        if self.behavior == "turn_right":
            self.lane_weight = [10000, 10000, 0]
            self.select_trajectory()
                
        # path publish
        self.global_path_pub.publish(self.global_path)
        self.trajectory_pub.publish(self.trajectory)
        # print(f"trajectory : {self.trajectory.x}")
        if len(self.generated_path) == 3:
            for i in range(1,4):
                globals()['lattice_path_{}_pub'.format(i)].publish(self.generated_path[i-1])


if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mp = Motion_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mp.run()
        rate.sleep()