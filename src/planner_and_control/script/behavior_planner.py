#!/usr/bin/env python3
import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String
from planner_and_control.msg import Ego
from lib.general_utils.read_global_path import read_global_path

class Behavior_Planner:
    def __init__(self):
        rospy.init_node('Behavior_Planner', anonymous = False)
        rospy.Subscriber('/state', String, self.state_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        self.pub = rospy.Publisher('/behavior', String, queue_size = 1)
        self.ego = Ego()
        self.state = String()
        self.behavior = ""

    def state_callback(self, msg):
        self.state = msg.data

    def ego_callback(self, msg):
        self.ego = msg
        
    def run(self):
        if self.state == "go":
            self.behavior = "go"
        if self.state == "obstacle detected":
            self.behavior = "obstacle avoidance"

        print(f"behavior_planner : {self.behavior}")
        self.pub.publish(self.behavior)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    bp = Behavior_Planner()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        bp.run()
        rate.sleep