#!/usr/bin/env python3
import rospy
# from lib.general_utils.ego import Ego
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Hander
from std_msgs.msg import String

class Behavior_Planner:
    def __init__(self):
        rospy.init_node('Behavior_Planner', anonymous = False)
        rospy.Subscriber('/state', String, self.state_callback)
        self.pub = rospy.Publisher('/behavior', String, queue_size = 1)
        # self.ego = Ego()

    def state_callback(self, msg):
        self.state = msg

    def run(self):
        # sample code
        a = 0
        b = 0
        if a == b:
            self.behavior = "go"
        #### sample code end
        print("#######")
        self.pub.publish(self.behavior)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Hander()
    bp = Behavior_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        bp.run()
        rate.sleep
