#!/usr/bin/env python3
import time
import csv
import threading
from math import hypot
from time import sleep

from localizer.ahrs import IMU
from localizer.gps import GPS
from localizer.dead_reckoning import DR

class Localizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.mapname = parent.args.map
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = self.shared.ego
        self.global_path = self.shared.global_path


        self.read_global_path() # only one time

        self.imu = IMU()
        self.gps = GPS()
        self.dr = DR()
        
    def read_global_path(self):
        with open(f"maps/{self.mapname}.csv", mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                self.global_path.x.append(float(line[0]))
                self.global_path.y.append(float(line[1]))
                # self.global_path.k.append(float(line[2]))
                # self.global_path.yaw.append(float(line[3]))

    def index_finder(self):
        min_dis = -1
        min_idx = 0
        step_size = 100
        save_idx = 0

        for i in range(max(self.ego.index - step_size, 0), self.ego.index + step_size):
            try:
                dis = hypot(self.global_path.x[i] - self.ego.x, self.global_path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i

        self.ego.index = min_idx


    def heading_decision(self):
        global time_sync
        main_time = time.time()
        time_sync = None

        if (main_time - self.gps.time) < 0.2 and (main_time - self.imu.time) < 0.2:
            time_sync = "Sync"
            if self.gps.heading_switch == True:
                offset = self.gps.heading - self.imu.heading
                self.ego.heading = self.imu.heading + offset
            else:
                self.ego.heading = self.imu.heading
        else:
            time_sync = "Unsync"
            self.ego.heading = self.imu.heading


    def run(self):
        while True:
            self.heading_decision()
            self.ego.x = self.gps.x
            self.ego.y = self.gps.y
            self.ego.dr_x = self.dr.x
            self.ego.dr_y = self.dr.y
            self.index_finder()

            # print("x : {0}, y : {1}, heading : {2}, switch : {3}, time sync : {4}, index : {5}"\
            # .format(self.ego.x, self.ego.y, self.ego.heading, self.gps.heading_switch, time_sync, self.ego.index))

            sleep(self.period)
