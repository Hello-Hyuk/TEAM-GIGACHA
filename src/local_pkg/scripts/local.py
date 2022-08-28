#!/usr/bin/env python3
import time
import rospy
import math
import argparse
from numpy import rad2deg
from local_pkg.msg import Local
from gps import GPS
from ahrs import IMU
from odometry import DR
from local_functions import quaternion_from_euler
from sig_int_handler import Activate_Signal_Interrupt_Handler


class Localization():
    def __init__(self, base):
        rospy.init_node('Localization', anonymous = False)
        self.pub = rospy.Publisher('/local_msgs', Local, queue_size = 1)
        self.msg = Local()
        self.base = base

        self.gps = GPS(self.base)
        self.imu = IMU()
        self.dr = DR()

        self.offset = 0
        self.heading = 0.0

        self.dr_init = False

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
        
        orientation = list(quaternion_from_euler(self.imu.roll, self.imu.pitch, self.heading))
        
        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.speed = self.dr.speed

        if self.gps.heading_switch:
            if not self.dr_init:
                self.msg.dr_x = self.gps.x
                self.msg.dr_y = self.gps.y
                self.dr_init = True
            
            self.msg.dr_x += self.dr.dis*math.cos(math.radians(self.heading))
            self.msg.dr_y += self.dr.dis*math.sin(math.radians(self.heading))
            
        self.msg.roll = self.imu.roll
        self.msg.pitch = self.imu.pitch
        self.msg.heading = self.heading
        self.msg.orientation.x = orientation[0]
        self.msg.orientation.y = orientation[1]
        self.msg.orientation.z = orientation[2]
        self.msg.orientation.w = orientation[3]

        self.pub.publish(self.msg)

        rospy.loginfo(self.msg)

if __name__=='__main__':
    Activate_Signal_Interrupt_Handler()

    parser = argparse.ArgumentParser()
    parser.add_argument('--base', '-b', nargs='*', help='base_names', default=[], dest='base_names')
    basename_input = parser.parse_args().base_names

    if len(basename_input) == 0:
        base_name = "Siheung"

    elif len(basename_input) == 1:
        base_name = basename_input[0]

    else:
        raise Exception('Invalid Arguments')

    loc = Localization(base_name)
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()