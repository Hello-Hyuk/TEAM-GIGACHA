#!/usr/bin/env python3
import rospy
import pymap3d

from planner_and_control.msg import Local
from planner_and_control.msg import Gngga
from lib.local_utils.imu import IMU

class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous=False)
        self.pub = rospy.Publisher('/pose', Local, queue_size = 1)
        self.msg = Local()

        self.x = 0
        self.y = 0
        rospy.Subscriber("/Gngga_raw", Gngga, self.gps_call_back)

        self.imu = IMU()

        # K-city
        self.lat_origin = 37.239231667
        self.lon_origin = 126.773156667
        self.alt_origin = 15.400

    def gps_call_back(self,data):
        self.x, self.y, _ = pymap3d.geodetic2enu(data.latitude, data.longitude, self.alt_origin, \
                                    self.lat_origin , self.lon_origin, self.alt_origin)

    def main(self):
        self.msg.x = self.x
        self.msg.y = self.y
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