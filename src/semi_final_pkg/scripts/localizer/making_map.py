#!/usr/bin/env python3
import threading
import rospy
from time import sleep
from math import hypot
from std_msgs.msg import Int64
from local_pkg.msg import Serial_Info
from .cubic_spline_planner import calc_spline_course

class MP(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        rospy.Subscriber('/Displacement_right', Int64, self.encoderCallback)
        rospy.Subscriber('/serial', Serial_Info, self.serialTopulse)
        self.period = 1.0 / rate
        self.global_path = parent.shared.global_path
        self.shared = parent.shared

        self.ego = parent.shared.ego

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
        self.temp = 0

        self.odometry_left = 0

        self.stop_thread = False
        self.right_switch = False


    def serialTopulse(self, data):  
        if self.init == 0: 
            self.init = int(data.encoder[0]) + int(data.encoder[1])*256 \
                 + int(data.encoder[2])*256**2 + \
                    int(data.encoder[3])*256**3 
 
        self.left = int(data.encoder[0]) + int(data.encoder[1])*256 \
             + int(data.encoder[2])*256**2 + \
                int(data.encoder[3])*256**3 - self.init 

        self.filter()

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
        if self.right_switch == False:
            self.right_init = msg.data
            self.right_switch = True

        self.right = msg.data - self.right_init

        self.pulse = (self.right_pulse + self.left_pulse) / 2
        
    def map_maker(self):
        self.global_path.x.append(self.ego.x)
        self.global_path.y.append(self.ego.y)
        self.temp = self.pulse

    def map_routine(self):
        x = []
        y = []
        x.append(self.global_path.x[-5])
        x.append(self.global_path.x[0])

        y.append(self.global_path.y[-5])
        y.append(self.global_path.y[0])

        cx, cy, _, _, _ = calc_spline_course(x, y, ds=0.1)

        self.global_path.x.extend(cx)
        self.global_path.y.extend(cy)
        
        for i in range(3):
            self.global_path.x.extend(self.global_path.x)
            self.global_path.y.extend(self.global_path.y)

    def run(self):
        while True:
            if not self.stop_thread:
                if round(self.pulse) % 6 == 0 and self.pulse !=self.temp:
                    self.map_maker()

                if len(self.global_path.x) >= 50 and hypot(self.ego.x, self.ego.y) <= 1.2:
                    self.stop_thread = True
                    self.map_routine()
                    print('====================2ND START====================')
                    self.shared.state = "2nd"
            else:
                sleep(self.period)