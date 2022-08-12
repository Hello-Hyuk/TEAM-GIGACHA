#!/usr/bin/env python3
import threading
import rospy
import pandas as pd
from time import sleep
from math import hypot
from std_msgs.msg import Int64
from sensor_msgs.msg import Imu
from localizer.gps import GPS


class MC(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.map_switch = False
        self.period = 1.0 / rate
        self.global_path = parent.shared.global_path
        self.shared = parent.shared

        self.ego = parent.shared.ego
        self.gps = GPS()

        self.right = 0  # pulse from sensor
        self.left = 0  # pulse from serial

        # for odometry
        self.init = 0
        self.flag_filter = True

        self.left_pulse = 0
        self.right_pulse = 0
        self.pulse = 0
        self.diff_left = 0
        self.diff_right = 0

        self.stop_thread = False
        self.right_switch = False
        self.temp = 0

        self.latitude = []
        self.longitude = []

        self.prev_lat = 0
        self.prev_lon = 0

        rospy.Subscriber('/Displacement_right', Int64, self.encoderCallback)
        rospy.Subscriber('/imu', Imu, self.map_csv)

    def serialTopulse(self):
        if self.init == 0:
            self.init = int(self.ego.encoder[0]) + int(self.ego.encoder[1])*256\
                + int(self.ego.encoder[2])*256**2 + \
                int(self.ego.encoder[3])*256**3

        odometry_left = int(self.ego.encoder[0]) + int(self.ego.encoder[1])*256\
            + int(self.ego.encoder[2])*256**2 + \
            int(self.ego.encoder[3])*256**3 - self.init

        return odometry_left

    def filter(self):
        if self.flag_filter:
            self.left_pulse = self.left
            self.right_pulse = self.right
            self.flag_filter = False

        if (abs(self.left - self.left_pulse) > 100):
            self.left_pulse = self.left + self.diff_left
        else:
            self.diff_left = self.left - self.left_pulse
            self.left_pulse = self.left

        if (abs(self.right - self.right_pulse) > 100):
            self.right_pulse = self.right + self.diff_right
        else:
            self.diff_right = self.right - self.right_pulse
            self.right_pulse = self.right

    def encoderCallback(self,msg):
        self.left = self.serialTopulse()
        if self.right_switch == False:
            self.right_init = msg.data
            self.right_switch = True

        self.right = msg.data - self.right_init

        self.filter()

        self.pulse = (self.right_pulse + self.left_pulse) / 2

    def map_maker(self):
        self.temp = self.pulse

        if self.gps.lat != self.prev_lat and self.gps.lon != self.prev_lon:
            self.latitude.append(self.gps.lat)
            self.longitude.append(self.gps.lon)

        self.prev_lat = self.gps.lat
        self.prev_lon = self.gps.lon

    def map_csv(self, msg):
        print('subscripve--------------------------------')
        if self.map_switch == False:
            save_data = list(zip(self.longitude, self.latitude))

            save_df = pd.DataFrame(save_data)
            save_df.to_csv("parking_1lane.csv", index = False, header = False)
            self.map_switch = True    

    def run(self):
        while True:
            if not self.stop_thread:
                if round(self.pulse) % 6 == 0 and self.pulse !=self.temp:
                    self.map_maker()
            else:
                sleep(self.period)