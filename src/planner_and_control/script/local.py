#!/usr/bin/env python3
import rospy
import pymap3d

from planner_and_control.msg import Local
from lib.local_utils.gps import GPS
from lib.local_utils.imu import IMU

class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous=False)
        self.pub = rospy.Publisher('/pose', Local, queue_size = 1)
        self.msg = Local()

        self.gps = GPS()
        self.imu = IMU()

    def main(self):
        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.heading = self.imu.yaw


        self.pub.publish(self.msg)

        print("Localization On...")

        # print("======x : {}".format(self.msg.x))
        # print("======y : {}".format(self.msg.y))
        # print("====yaw : {}".format(self.msg.heading))

if __name__ == '__main__':
    loc = Localization()
    rate = rospy.Rate(50)
 
    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()