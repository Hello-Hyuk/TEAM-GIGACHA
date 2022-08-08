#!/usr/bin/env python3
import time
import csv
import threading
import math
import rospy
from local_pkg.msg import Local
from math import hypot, atan2
from time import sleep, time
from numpy import rad2deg[]


class Localizer(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        rospy.init_node('main', anonymous=False)

        rospy.Subscriber('/local_msgs', Local, self.local_callback)
        self.mapname = parent.args.map
        self.period = 1.0 / rate

        self.ego = parent.shared.ego
        self.global_path = parent.shared.global_path
        self.parking = parent.shared.park

        self.read_global_path()  # only one time

    def local_callback(self, msg):
        self.ego.x = self.msg.x
        self.ego.y = self.msg.y
        self.ego.heading = self.msg.heading
        self.ego.orientaion = self.msg.orientation
        self.ego.dr_x = self.msg.dr_x
        self.ego.dr_y = self.msg.dr_y

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
        # save_idx = self.ego.index                    # for not decreasing index
        save_idx = 0
        for i in range(max(self.ego.index - step_size, 0), self.ego.index + step_size):
            try:
                dis = hypot(
                    self.global_path.x[i] - self.ego.x, self.global_path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i
        self.ego.index = min_idx

    def run(self):
        while True:
            self.index_finder()

            sleep(self.period)
