#!/usr/bin/env python3
import rospy

from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
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

        # print("Localization On...")

        print("=========Localization=========")
        print(f"x : {self.msg.x}")
        print(f"y : {self.msg.y}")
        print(f"heading : {self.msg.heading}")

if __name__ == '__main__':
    Activate_Signal_Interrupt_Handler()
    loc = Localization()
    rate = rospy.Rate(50)
 
    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()