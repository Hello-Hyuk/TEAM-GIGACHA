import threading
from time import sleep
from math import pi, degrees, radians
import numpy as np

class Stanley(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego
        self.plan = parent.shared.plan

        self.lattice_path = parent.shared.lattice_path
 
        self.WB = 1.04 # wheel base
        self.k = -0.05

        self.cx = self.shared.global_path.x
        self.cy = self.shared.global_path.y
        self.cyaw = self.shared.global_path.k

        self.current_target_idx = 0
        self.error_front_axle = 0

        self.target_idx = 0
        self.error_front_axle = 0

        self.theta_e = 0
        self.theta_d = 0

    def calc_target_index(self):
        # Calc front axle position
        fx = self.ego.x + self.WB * np.cos(radians(self.ego.heading))
        fy = self.ego.y + self.WB * np.sin(radians(self.ego.heading))

        # Search nearest point index
        dx = [fx - icx for icx in self.cx]
        dy = [fy - icy for icy in self.cy]
        d = np.hypot(dx, dy)
        self.target_idx = np.argmin(d)
        # print(self.target_idx)
        # Project RMS error onto front axle vector
        front_axle_vec = [-np.cos(radians(self.ego.heading) + np.pi / 2),
                        -np.sin(radians(self.ego.heading) + np.pi / 2)]
        self.error_front_axle = np.dot([dx[self.ego.index], dy[self.ego.index]], front_axle_vec)

    def normalize_angle(self):
        angle = self.cyaw[self.ego.index] - (radians(self.ego.heading))

        while angle > np.pi:
            angle -= 2.0 * np.pi

        while angle < -np.pi:
            angle += 2.0 * np.pi
        
        # theta_e corrects the heading error
        # theta_d corrects the cross track error
        self.theta_e = angle
        self.theta_d = np.arctan2(self.k * self.error_front_axle, self.ego.speed)

    def run(self):
        while True:
            
            self.calc_target_index() #  target course
            self.normalize_angle()
            print("heading error : ", degrees(self.theta_e))
            print("cross track error : ", degrees(self.theta_d))
            
            delta = self.theta_e + self.theta_d # Steering control
            # print(degrees(delta))
            self.ego.input_steer = max(min(degrees(delta), 27.0), -27.0)
            # self.ego.input_steer = delta
            sleep(self.period)


