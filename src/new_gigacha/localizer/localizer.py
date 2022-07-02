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
        self.global_path = parent.shared.global_path
        self.odometry = parent.shared.dp #displacement [pulse]

        self.read_global_path() # only one time

        self.imu = IMU()
        self.gps = GPS()

        self.x = self.gps.x
        self.y = self.gps.y # initialize
        
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

    def dead_reckoning(self):
        if self.flag:
            self.a = self.odometry.left
            self.b = self.odometry.left
            self.c = self.odometry.right
            self.d = self.odometry.right
            self.flag = False

        elif self.flag == False:
            self.a = self.b
            self.b = self.odometry.left

            self.c = self.d
            self.d = self.odometry.right

        if ((self.b - self.a) < -10000000):
            dis_left = (self.b + (256**4 - self.a))/60.852 # pulse to meter
        else:
            dis_left = (self.b - self.a)/60.852 # 1.6564/100

        if ((self.d - self.c) < -10000000):
            dis_right = (self.d + (256**4 - self.a))/60.852
        else:
            dis_right = (self.d - self.c)/60.852

        dis = (dis_right + dis_left) / 2

        self.velocity = dis/0.1

        self.x += dis*math.cos(math.radians(self.imu.heading))
        self.y += dis*math.sin(math.radians(self.imu.heading))

        self.ego.dr_x = self.x
        self.ego.dr_y = self.y

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
            self.dead_reckoning()
            self.index_finder()

            # print("x : {0}, y : {1}, heading : {2}, switch : {3}, time sync : {4}, index : {5}"\
            # .format(self.ego.x, self.ego.y, self.ego.heading, self.gps.heading_switch, time_sync, self.ego.index))

            sleep(self.period)