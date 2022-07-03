#!/usr/bin/env python3
import rospy
from local_pkg.msg import Displacement

class Odometry():
    def __init__(self):
        rospy.Subscriber('/encoder', Displacement, self.encoderCallback)
        self.right = 0
        self.left = 0

    def encoderCallback(self, msg):
        self.right = msg.data

if __name__ == '__main__':
    try:
        odometry=Odometry()
    except rospy.ROSInterruptException:
        pass