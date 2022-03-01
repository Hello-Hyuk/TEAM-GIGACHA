#!/usr/bin/env python3
import rospy
from math import sqrt
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String
from planner_and_control.msg import Ego

class Mission_Planner:
    def __init__(self):
        rospy.init_node('Mission_Planner', anonymous = False)
        self.pub = rospy.Publisher('/state', String, queue_size = 1)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/', , self.lidar_callback)
        self.ego = Ego()
        self.state = ''
        self.obs_dis

    def ego_callback(self, msg):
        self.ego = msg

    def lidar_callback(self, msg):
        self.obstacle = msg
        self.obs_dis = sqrt(self.obstacle.x**2 + self.obstacle.y**2)
        
    def run(self):
        if self.obs_dis < 10 : 
            self.state = "obstacle detected"
        else :
            self.state = "go"
        print(f"mission_planner : {self.state}")
        self.pub.publish(self.state)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mm = Mission_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mm.run()
        rate.sleep()