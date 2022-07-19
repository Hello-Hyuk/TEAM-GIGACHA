import pymap3d
import json
from shared.path import Path
from math import cos, degrees, radians, sin, atan2, sqrt, hypot
from numpy import rad2deg
import csv
class Parking_Motion():
    def __init__(self, sh, pl, eg):
        self.shared = sh
        self.plan = pl
        self.ego = eg

        self.global_path = self.shared.global_path
        self.parking = self.shared.park

        self.mapname = ''
        self.cnt = False
        
#########saved map import function########
    def make_parking_tra(self):
        # self.mapname = str(self.parking.select_num)
<<<<<<< Updated upstream
        self.parking.select_num = 3
=======
        # self.parking.select_num = 
>>>>>>> Stashed changes
        # self.mapname = 'parkssang'+ str(self.parking.select_num)
        path1 = Path()
        path2 = Path()
        min_index = 0
        min_dis = 10000000

        # with open(f"maps/kcity_parking/{self.mapname}.csv", mode="r") as csv_file:
        with open(f"maps/inha_parking/{str(self.parking.select_num)}.csv", mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                path1.x.append(float(line[0]))
                path1.y.append(float(line[1]))
                # self.global_path.k.append(float(line[2]))
                # self.global_path.yaw.append(float(line[3]))
        path1.x, path1.y = list(reversed(path1.x)), list(reversed(path1.y))

        for i in range(len(self.global_path.x)):
            dx = path1.x[0] - self.global_path.x[i]
            dy = path1.y[0] - self.global_path.y[i]
            dis = sqrt(dx*dx + dy*dy)
            if dis < min_dis:
                min_dis = dis
                min_index = i

        # self.parking.mindex = min_index - 20
        self.parking.mindex = min_index


        if self.parking.select_num == 1:
            # for i in range(self.parking.mindex, self.parking.mindex - 15, -1):
            for i in range(self.parking.mindex, self.parking.mindex - 5, -1):
                path1.x.insert(0,self.global_path.x[i])
                path1.y.insert(0,self.global_path.y[i])
            # path1.x, path1.y = path1.x[0:90], path1.y[0:90]
        else:
            # for i in range(self.parking.mindex, self.parking.mindex - 20, -1):
            for i in range(self.parking.mindex, self.parking.mindex - 25, -1):
                path1.x.insert(0,self.global_path.x[i])
                path1.y.insert(0,self.global_path.y[i])
            path1.x, path1.y = path1.x[0:70], path1.y[0:70]

        path2.x, path2.y = list(reversed(path1.x)), list(reversed(path1.y))
        self.parking.forward_path = path1
        self.parking.backward_path = path2
        


    def park_index_finder(self,path):
        min_dis = -1
        min_idx = 0
        step_size = 10
        save_idx = self.parking.index

        for i in range(max(self.parking.index - step_size, 0), self.parking.index + step_size):
            try:
                dis = hypot(
                    path.x[i] - self.ego.x, path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i

        return min_idx

    def parking_drive(self, direction):
        self.parking.on = True
        self.parking.direction = direction

        if self.parking.direction == 2:
            if self.cnt == False:
                self.parking.index = 0
                self.cnt = True
            path = self.parking.backward_path
        else:
            path = self.parking.forward_path

        self.parking.index = self.park_index_finder(path)
        self.parking.stop_index = len(path.x)