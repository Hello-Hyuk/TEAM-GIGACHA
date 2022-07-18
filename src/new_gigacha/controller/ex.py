import threading
from time import sleep
from math import pi, degrees, radians, atan2
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

        self.error_front_axle = 0

        self.heading_term = 0
        self.cte_term = 0

    def make_curvature(name):
        with open('/home/gigacha/TEAM-GIGACHA/src/semi_final_pkg/maps/kcity_simul/final.csv') as csv_file:
            csv_reader = pd.read_csv(csv_file, delimiter = ',', names = ['x', 'y', 'yaw', 'curvature', 'distance'])

            x_list = csv_reader['x'].values.tolist()
            y_list = csv_reader['y'].values.tolist()
            yaw_list = []
            curvature_list = []

            for i in range(len(x_list)-1):
                yaw = atan2(y_list[i] - y_list[i-1], x_list[i] - x_list[i-1])
                yaw_list.append((np.rad2deg(yaw)) % 360)

                if i == 0:
                    x_vals = [x_list[-1], x_list[0], x_list[1]]
                    y_vals = [y_list[-1], y_list[0], y_list[1]]
                    R = circumradius(x_vals, y_vals)
                    try:
                        curvature_list.append(1/R)
                    except ZeroDivisionError:
                        curvature_list.append(0)
                else:
                    R = circumradius(x_list[i-1:i+2], y_list[i-1:i+2])
                    try:
                        curvature_list.append(1/R)
                    except ZeroDivisionError:
                        curvature_list.append(0)


    def circumradius(xvals, yvals):
        x1, x2, x3, y1, y2, y3 = xvals[0], xvals[1], xvals[2],\
        yvals[0], yvals[1], yvals[2]

        den = 2 * ((x2-x1) * (y3-y2)-(y2-y1) * (x3-x2))
        num = ( (((x2-x1)**2) + ((y2-y1)**2)) * (((x3-x2)**2) + ((y3-y2)**2)) * (((x1-x3)**2) + ((y1-y3)**2)) )**0.5

        if den == 0:
            return 0
        
        r = abs(num/den)

        return r

    def normalize_angle(self, angle):
        while angle > np.pi:
            angle -= 2.0 * np.pi

        while angle < -np.pi:
            angle += 2.0 * np.pi


    def run(self):
        while True:
            self.make_curvature(final)
            heading_error = self.curvature_list[self.ego.index] - (radians(self.ego.heading))
            perp_vec = [-np.cos(radians(self.ego.heading) + np.pi / 2), -np.sin(radians(self.ego.heading) + np.pi / 2)]
            cte = np.dot([dx[self.ego.index], dy[self.ego.index]], perp_vec)
            self.normalize_angle(heading_error)

            self.heading_term = angle
            self.cte_term = np.atan2(self.k * cte, self.ego.speed)

            print("heading error : ", degrees(self.heading_term))
            print("cross track error : ", degrees(self.cte_term))
            
            delta = self.heading_term + self.cte_term # Steering control
            # print(degrees(delta))
            self.ego.input_steer = max(min(degrees(delta), 27.0), -27.0)
            # self.ego.input_steer = delta

            sleep(self.period)



