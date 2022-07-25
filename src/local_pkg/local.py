#!/usr/bin/env python3
import time
from math import hypot, atan2
from numpy import rad2deg
from local_pkg.msg import Local
from local_pkg.msg import Serial_Info
from scripts.gps import GPS
from scripts.ahrs import IMU
from scripts.odometry import DR
from scripts.local_functions import quaternion_from_euler

class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous = False)
        self.pub = rospy.Publisher('/local_msgs', Local, queue_size = 1)
        self.msg = Local()

        self.gps = GPS()
        self.imu = IMU()
        self.dr = DR()

        self.offset = 0
        self.heading = 0.0

    def heading_decision(self):
        global time_sync
        main_time = time.time()
        time_sync = None

        if self.dr.gear == 0:

            if (main_time - self.gps.time) < 0.2 and (main_time - self.imu.time) < 0.2:
                time_sync = "Sync"
                if self.gps.heading_switch == True:
                    self.offset = self.gps.heading - self.imu.heading
                    self.heading = self.imu.heading + self.offset
                else:
                    self.heading = self.imu.heading + self.offset
            else:
                time_sync = "Unsync"
                self.heading = self.imu.heading + self.offset

        else:
            self.heading = self.imu.heading + self.offset

    def main(self):
        self.heading_decision()
        
        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.heading = self.heading
        self.msg.dr_x += self.dr.dis*math.cos(math.radians(self.heading))
        self.msg.dr_y += self.dr.dis*math.sin(math.radians(self.heading))
        self.msg.orientation = quaternion_from_euler(self.imu.roll, self.imu.pitch, self.heading)

        self.pub.publish(self.msg)

if __name__=='__main__':
    loc = Localization()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()