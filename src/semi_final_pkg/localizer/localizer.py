#!/usr/bin/env python3
import time
import csv
import threading
import math
from math import hypot
from time import sleep

from localizer.ahrs import IMU
from localizer.gps import GPS


class Localizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.mapname = parent.args.map
        self.period = 1.0 / rate

        self.ego = parent.shared.ego

        self.gps = GPS()
        self.imu = IMU()

        self.offset = 0

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
            self.heading_decision()
            self.ego.x = self.gps.x
            self.ego.y = self.gps.y

            sleep(self.period)