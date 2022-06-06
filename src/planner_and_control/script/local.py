#!/usr/bin/env python3
import rospy

from std_msgs.msg import Time
from planner_and_control.msg import Local
from lib.local_utils.gps import GPS
from lib.local_utils.imu import IMU

class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous=False)
        self.pub = rospy.Publisher('/pose', Local, queue_size = 1)
        rospy.loginfo("============Localization On============")

        self.msg = Local()

        self.gps = GPS()
        self.imu = IMU()

    def main(self):
        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.heading = self.imu.heading
        self.msg.orientation = self.imu.orientation_q
        self.pub.publish(self.msg)

if __name__ == '__main__':
    loc = Localization()
    rospy.Subscriber("/timer", Time, loc.main)