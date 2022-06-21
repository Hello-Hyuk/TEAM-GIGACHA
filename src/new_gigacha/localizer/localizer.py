#!/usr/bin/env python3
from localizer.read_global_path import read_global_path
import rospy
import time
from std_msgs.msg import Time
from planner_and_control.msg import Local
from lib.local_utils.gps import GPS
from lib.local_utils.imu import IMU
from lib.local_utils.dead_reckoning import DR

import csv

import threading
from time import sleep

class Localizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.mapname = parent.args.map
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.global_path = self.shared.global_path
        self.read_global_path()
        
    def read_global_path(self):
        with open(f"maps/{self.mapname}.csv", mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                self.glboal_path.x.append(float(line[0]))
                self.glboal_path.y.append(float(line[1]))
                self.glboal_path.k.append(float(line[2]))
                self.glboal_path.yaw.append(float(line[3]))


    def run(self):
        while True:
            self.ego.speed = 1
            sleep(self.period)





class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous=False)

        self.pub = rospy.Publisher('/pose', Local, queue_size = 1)
        rospy.loginfo("============Localization On============")

        self.msg = Local()

        self.gps = GPS()
        self.imu = IMU()
        self.dr = DR()

    def main(self, data):
        main_time = time.time()
        time_sync = None

        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.dr_x = self.dr.x
        self.msg.dr_y = self.dr.y
        self.msg.dr_vel = self.dr.velocity
        self.msg.orientation = self.imu.orientation_q

        if (main_time - self.gps.time) < 0.2 and (main_time - self.imu.time) < 0.2: # time syncronize
            time_sync = "Sync"
            if self.gps.heading_switch == True:
                offset = self.gps.heading - self.imu.heading
                self.msg.heading = self.imu.heading + offset # heading correction with gps heading
            else:
                self.msg.heading = self.imu.heading
        else:
            time_sync = "Unsync"
            self.msg.heading = self.imu.heading
        
        self.pub.publish(self.msg)

        print("======================")
        print("x : {0}, y : {1}".format(self.msg.x, self.msg.y))
        print("heading : {0}".format(self.msg.heading))
        print("velocity : {0}".format(self.msg.dr_vel))
        print("switch : {0}".format(self.gps.heading_switch))
        print("time sync : {0}".format(time_sync))

if __name__ == '__main__':
    loc = Localization()
    rospy.Subscriber("/timer", Time, loc.main)
    rospy.spin()