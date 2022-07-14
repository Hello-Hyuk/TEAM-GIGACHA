#!/usr/bin/env python3
import rospy
from .sig_int_handler import ActivateSignalInterruptHandler
from planner_and_control.msg import Perception

class Input:
    def __init__(self):
        rospy.init_node('Input', anonymous = False)
        self.pub = rospy.Publisher("/input", Perception, queue_size = 1)
        self.perception = Perception()
        self.perception.objx = [3]####
        self.perception.objy = [3]####
        self.perception.objr = []####
        
    def run(self):
        self.pub.publish(self.perception)

if __name__ == "__main__":
    ActivateSignalInterruptHandler()
    ss = Input()
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        ss.run()
        rate.sleep()