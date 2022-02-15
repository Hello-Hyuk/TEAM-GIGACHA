#!/usr/bin/env python3
import rospy
from lib.general_utils.ego import Ego
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Hander
from std_msgs.msg import String

class Mission_Planner:
    def __init__(self):
        rospy.init_node('Mission_Planner', anonymous = False)
        self.pub = rospy.Publisher('/state', String, queue_size = 1)
        self.ego = Ego()
        self.state = ""

    def run(self):
        # sample code
        a = 0
        b = 0
        if a == b:
            self.state = "go"
        #### sample code end

        pub.publish(self.state)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Hander()
    mm = Mission_Planner()
    if not rospy.is_shutdown():
        mm.run()
