#!/usr/bin/env python3
import sys
import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.general_utils.read_global_path import read_global_path
from lib.planner_utils.find_local_path import findLocalPath
from lib.planner_utils.LPP import path_maker
from planner_and_control.msg import Path as CustomPath
from planner_and_control.msg import Ego
from planner_and_control.msg import Obj
from std_msgs.msg import String
from nav_msgs.msg import Path
from math import sqrt

class Motion_Planner:
    def __init__(self):
        rospy.init_node('Motion_Planner', anonymous = False)
        arg = rospy.myargv(argv=sys.argv)
        self.path_name=arg[1]

        rospy.Subscriber('/behavior', String, self.behavior_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/obj', Obj, self.obj_callback)

        self.global_path_pub = rospy.Publisher('/global_path', CustomPath, queue_size = 1)
        self.local_path_pub = rospy.Publisher('/lattice_path', CustomPath, queue_size = 1)
        self.trajectory_pub = rospy.Publisher('/local_path', CustomPath, queue_size = 1)

        # rviz
        for i in range(1,6):
            globals()['lattice_path_{}_pub'.format(i)] = rospy.Publisher('lattice_path_{}'.format(i),Path,queue_size=1) 

        self.ego = Ego()
        self.behavior = ''
        self.global_path = CustomPath()
        self.generated_path = Path()
        self.trajectory_name = ""

        self.global_path = read_global_path('ex')

        self.ego_speed = 0
        self.current_lane = 0
        self.obj = Obj()

    def behavior_callback(self, msg):
        self.behavior = msg.data

    def ego_callback(self, msg):
        self.ego = msg

    def obj_callback(self, msg):
        self.obj = msg

    def run(self):
        current_lane = input("current lane(left : 1, right : 2) : ") # temporary code(to aviod lidar dectection)
        self.local_path = findLocalPath(self.global_path, self.ego) # local path (50)
        self.generated_path = path_maker(self.local_path, self.ego) # lattice paths

        trajectory = CustomPath()

        if self.behavior == "go":
            self.trajectory = read_global_path(self.path_name)
            self.trajectory_name = "global_path"

        if self.behavior == "obstacle avoidance":
            if current_lane == 1:
                a = 10000
                b = 0
            else:
                a = 0
                b = 10000
            lane_weight = [a, 0, b]
            
            obs_dis = sqrt((self.ego.x - self.obj.x)**2 + (self.ego.y - self.obj.y)**2)

            if obs_dis < 10:
                for i in range (len(self.generated_path)):
                    distance = sqrt((self.generated_path[i].poses[-1].pose.position.x - self.obj.x)**2
                                    + (self.generated_path[i].poses[-1].pose.position.y - self.obj.y)**2)
                    lane_weight[i] +=  distance
                lane_weight[2] = 100
                lane_weight[1] = 10000

            self.selected_lane = lane_weight.index(min(lane_weight))
            self.local_path = self.generated_path[self.selected_lane]
            self.trajectory_name = self.selected_lane

            print(f"obs_dis : {obs_dis}")
            print(f"lane_weight : {lane_weight}")
            print(f"motion_planner : {self.trajectory_name}, local_path")

        for i in range (len(self.local_path.poses)):
            trajectory.x.append(self.local_path.poses[i].pose.position.x)
            trajectory.y.append(self.local_path.poses[i].pose.position.y)
    
        # rviz
        if len(self.generated_path) == 5:                    
            for i in range(1,6):
                globals()['lattice_path_{}_pub'.format(i)].publish(self.generated_path[i-1])
                
        # path publish
        self.global_path_pub.publish(self.global_path)
        self.trajectory_pub.publish(trajectory)
if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mp = Motion_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mp.run()
        rate.sleep()