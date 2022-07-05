import threading
import math
from time import sleep

from localizer.odometry import Odometry
from localizer.gps import GPS
from localizer.ahrs import IMU

class DR(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.ego = parent.shared.ego
        
        self.gps = GPS()
        self.imu = IMU()
        self.odometry = Odometry() # right / left wheel pulse

        self.ego.dr_x = self.gps.x # initial position
        self.ego.dr_y = self.gps.y # initial position

        self.flag_filter = True
        self.flag_dr = True
        self.init = 0

        self.diff_left = 0
        self.diff_right = 0

        self.left_pulse = 0
        self.right_pulse = 0

        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0

    def serialTopulse(self):
        if self.init ==0:
            self.init = int(self.ego.encoder[0]) + int(self.ego.encoder[1])*256\
                + int(self.ego.encoder[2])*256**2 + int(self.ego.encoder[3])*256**3

        self.odometry.left = int(self.ego.encoder[0]) + int(self.ego.encoder[1])*256\
            + int(self.ego.encoder[2])*256**2 + int(self.ego.encoder[3])*256**3 - self.init

    def filter(self):
        if self.flag_filter:
            self.left_pulse = self.odometry.left
            self.right_pulse = self.odometry.right
            self.flag_filter = False

        if (abs(self.odometry.left - self.left_pulse) > 100):
            self.left_pulse = self.odometry.left + self.diff_left
        else:
            self.diff_left = self.odometry.left - self.left_pulse
            self.left_pulse = self.odometry.left

        if (abs(self.odometry.right - self.right_pulse) > 100):
            self.right_pulse = self.odometry.right + self.diff_right
        else:
            self.diff_right = self.odometry.right - self.right_pulse
            self.right_pulse = self.odometry.right

    def dead_reck(self):
        if self.flag_dr:
            self.a = self.left_pulse
            self.b = self.left_pulse
            self.c = self.right_pulse
            self.d = self.right_pulse
            self.flag_dr = False

        elif self.flag_dr == False:
            self.a = self.b
            self.b = self.left_pulse

            self.c = self.d
            self.d = self.right_pulse

        if ((self.b - self.a) < -10000000):
            self.ego.dis_left = (self.b + (256**4 - self.a))/60.852 # pulse to meter
        else:
            self.ego.dis_left = (self.b - self.a)/60.852 # 1.6564/100

        if ((self.d - self.c) < -10000000):
            self.ego.dis_right = (self.d + (256**4 - self.c))/60.852 # pulse to meter
        else:
            self.ego.dis_right = (self.d - self.c)/60.852 # 1.6564/100

        dis = (self.ego.dis_left + self.ego.dis_right) / 2


        self.ego.dr_x += dis*math.cos(math.radians(self.imu.heading))
        self.ego.dr_y += dis*math.sin(math.radians(self.imu.heading))

    def run(self):
        while True:
            self.serialTopulse()
            self.filter()
            self.dead_reck()

            sleep(self.period)