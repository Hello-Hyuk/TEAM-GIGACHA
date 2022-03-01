#!/usr/bin/env python3
import rospy
from lib.general_utils.read_global_path import read_global_path
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String
from planner_and_control.msg import Path
from planner_and_control.msg import Ego

class Motion_Planner:
    def __init__(self):
        rospy.init_node('Motion_Planner', anonymous = False)
        rospy.Subscriber('/behavior', String, self.behavior_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        self.pub = rospy.Publisher('/trajectory', Path, queue_size = 1)
        self.ego = Ego()
        self.behavior = ''
        self.trajectory = Path()
        self.trajectory_name = ""
    
    def behavior_callback(self, msg):
        self.behavior = msg.data

    def ego_callback(self, msg):
        self.ego = msg
        
    def run(self):
        self.trajectory = read_global_path('ex')
        self.trajectory_name = "global_path"
        
        print(f"motion_planner : {self.trajectory_name}")
        self.pub.publish(self.trajectory)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mp = Motion_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mp.run()
        rate.sleep()