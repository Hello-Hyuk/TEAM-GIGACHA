#!/usr/bin/env python3
import threading
import rospy
from time import sleep
from math import hypot
from std_msgs.msg import Int64
from localizer.gps import GPS

class MP(threading.Thread):
    def __init__(self, parent, rate):
        rospy.Subscriber('/Displacement_right', Int64, self.encoderCallback)
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
        self.right = msg.data

        self.filter()

        self.pulse = (self.right_pulse + self.left_pulse) / 2

    def map_maker(self):
        self.global_path.x.append(self.gps.x)
        self.global_path.y.append(self.gps.y)

    def run(self):
        while True:
            if not self.stop_thread:
                if round(self.pulse) % 6 == 0:
                    self.map_maker()

                if len(self.global_path.x) >= 100 and hypot(self.gps.x, self.gps.y) <= 0.96:
                    self.stop_thread = True
                    self.shared.state = "2nd"
            else:
                sleep(self.period)