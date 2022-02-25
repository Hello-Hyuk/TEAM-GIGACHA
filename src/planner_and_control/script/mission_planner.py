#!/usr/bin/env python3
import rospy
from lib.planner_utils.index_finder import IndexFinder
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String
from planner_and_control.msg import Ego

class Mission_Planner:
    def __init__(self):
        rospy.init_node('Mission_Planner', anonymous = False)
        self.pub = rospy.Publisher('/state', String, queue_size = 1)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        self.ego = Ego()
        self.state = ''

    def ego_callback(self, msg):
        self.ego = msg
        
    def run(self):
        a = 0
        b = 0
        if a == b:
            self.state = "go"
        #### sample code end

        print(f"mission_planner : {self.state}")
        self.pub.publish(self.state)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mm = Mission_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mm.run()
        rate.sleep()