#!/usr/bin/env python3
import time
import threading
import numpy as np
from math import atan2
from time import sleep
from .local_functions import circumradius

from localizer.ahrs import IMU
from localizer.gps import GPS


class Localizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.mapname = parent.args.map
        self.period = 1.0 / rate

        self.ego = parent.shared.ego
        self.shared = parent.shared
        self.global_path = parent.shared.global_path

        self.gps = GPS()
        self.imu = IMU()

        self.offset = 0
        self.switch = True

    def add_curvature_yaw(self):
        for i in range(len(self.global_path.x)-1):
            yaw = atan2(self.global_path.y[i]-self.global_path.y[i-1],\
            self.global_path.x[i]-self.global_path.x[i-1])
            self.global_path.yaw_list.append((np.rad2deg(yaw)) % 360) # enu coordinate

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
        
        self.global_path.x.pop()
        self.global_path.y.pop()

    def heading_decision(self):
        global time_sync
        main_time = time.time()
        time_sync = None

        if (main_time - self.gps.time) < 0.2 and (main_time - self.imu.time) < 0.2:
            time_sync = "Sync"
            if self.gps.heading_switch == True:
                self.offset = self.gps.heading - self.imu.heading
                self.ego.heading = self.imu.heading + self.offset
            else:
                self.ego.heading = self.imu.heading + self.offset
        else:
            time_sync = "Unsync"
            self.ego.heading = self.imu.heading + self.offset

    def run(self):
        while True:
            if self.shared.state == "2nd" and self.switch:
                self.add_curvature_yaw()
                self.switch = False

            self.heading_decision()
            self.ego.x = self.gps.x
            self.ego.y = self.gps.y

            sleep(self.period)