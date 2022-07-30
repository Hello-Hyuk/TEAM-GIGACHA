#!/usr/bin/env python3
import threading
import rospy
from time import sleep
from math import hypot
from local_pkg.msg import Local

class MP(threading.Thread):
    def __init__(self, parent, rate):
        rospy.Subscriber('/local_msgs', Local, self.localCallback)
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.global_path = parent.shared.global_path
        self.ego = parent.shared.ego

        self.pulse = 0.0

        self.stop_thread = False

    def localCallback(self, msg):
        self.ego.x = msg.x
        self.ego.y = msg.y
        self.ego.heading = msg.heading
        self.pulse = msg.distance

    def calculate_yaw_curvature(self):
        for i in range(len(self.global_path.x)-1):
            yaw = atan2(self.global_path.y[i] - self.global_path.y[i-1], self.global_path.x[i] - self.global_path.x[i-1])
            self.global_path.yaw_list.append((np.rad2deg(yaw)) % 360)

            if i == 0:
                x_vals = [self.global_path.x[-1], self.global_path.x[0], self.global_path.x[1]]
                y_vals = [self.global_path.y[-1], self.global_path.y[0], self.global_path.y[1]]
                R = circumradius(x_vals, y_vals)
                try:
                    self.global_path.curvature.append(1/R)
                except ZeroDivisionError:
                    self.global_path.curvature.append(0)
            else:
                R = circumradius(self.global_path.x[i-1:i+2], self.global_path.y[i-1:i+2])
                try:
                    self.global_path.curvature.append(1/R)
                except ZeroDivisionError:
                    self.global_path.curvature.append(0)

    def map_maker(self):
        self.global_path.x.append(self.ego.x)
        self.global_path.y.append(self.ego.y)

    def run(self):
        while True:
            if not self.stop_thread:
                if round(self.pulse) % 6 == 0:
                    self.map_maker()

                if len(self.global_path.x) >= 100 and hypot(self.ego.x, self.ego.y) <= 0.96:
                    self.stop_thread = True
                    self.calculate_yaw_curvature()
                    self.shared.state = "2nd"
            else:
                sleep(self.period)