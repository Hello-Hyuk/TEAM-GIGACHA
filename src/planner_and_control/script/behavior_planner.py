#!/usr/bin/env python3
import rospy
from lib.general_utils.ego import Ego
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String

class Behavior_Planner:
    def __init__(self):
        rospy.init_node('Behavior_Planner', anonymous = False)
        rospy.Subscriber('/state', String, self.state_callback)
        self.pub = rospy.Publisher('/behavior', String, queue_size = 1)
        self.ego = Ego()
        self.state = ""
        self.behavior = ""

    def state_callback(self, msg):
        self.state = msg

    def run(self):
        if self.state == "go":
            self.behavior = "go"

        print("behavior_planner")
        self.pub.publish(self.behavior)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    bp = Behavior_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        bp.run()
        rate.sleep
