#!/usr/bin/env python3
from socket import MsgFlag
import rospy
from lib.general_utils.read_global_path import read_global_path
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.planner_utils.LPP import LatticePlanner
from lib.planner_utils.find_local_path import findLocalPath
from lib.planner_utils.index_finder import IndexFinder
from std_msgs.msg import String
from planner_and_control.msg import Path
from planner_and_control.msg import Ego
from sensor_msgs.msg import PointCloud


class Motion_Planner:
    def __init__(self):
        rospy.init_node('Motion_Planner', anonymous = False)
        rospy.Subscriber('/behavior', String, self.behavior_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/obj',PointCloud,self.obj_callback)
        self.pub = rospy.Publisher('/trajectory', Path, queue_size = 1)
        self.ego = Ego()
        self.behavior = ''
        self.trajectory = Path()
        self.trajectory_name = ""
        self.ego_speed = 0
        self.ego_status = []
        self.current_lane = 0
        
    
    def behavior_callback(self, msg):
        self.behavior = msg.data

    def ego_callback(self, msg):
        self.ego = msg
        self.ego_status = [self.ego.x, self.ego.y, self.ego.heading]

    def obj_callback(self,msg):
        self.obj=msg

        
    def run(self):

        if self.behavior == "go":
            self.trajectory = read_global_path('ex')
            self.trajectory_name = "global_path"

        if self.behavior == "obstacle avoidance":
            self.local_path=findLocalPath(self.trajectory,self.ego)
            self.current_waypoint=IndexFinder
           

            self.lattice_path,self.selected_lane = LatticePlanner(self.local_path, self.obj , self.ego_status, self.ego.speed, self.current_lane)
            self.current_lane=self.selected_lane

            
            if self.selected_lane != -1: 
                self.local_path=self.lattice_path[self.selected_lane]               


        
        print(f"motion_planner : {self.trajectory_name}")
        self.pub.publish(self.trajectory)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mp = Motion_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mp.run()
        rate.sleep()