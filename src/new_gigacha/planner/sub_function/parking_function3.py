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

        #simul kcity
        self.base_lat = 37.239231667
        self.base_lon = 126.773156667
        self.base_alt = 15.4

        self.smooth_radius = 5
        self.mapname = ''
        self.cnt = False
        with open('/home/gigacha/TEAM-GIGACHA/src/new_gigacha/localizer/parking_KCity2.json') as pkc:
            self.parking_point = json.load(pkc)
        
#########saved map import function########
    def make_parking_tra(self):
        # self.point = self.parking_point[str(self.parking.select_num)]
        self.point = self.parking_point[str(7)]
        self.start_point = self.point["start"]
        self.end_point = self.point["end"]
        if len(self.parking.forward_path.x) == 0:
            self.parking.forward_path, self.parking.backward_path = self.findParkingPath()


    def findParkingPath(self):
        min_index = 0
        min_dis = 10000000

        self.parking_x, self.parking_y = self.parking_call_back(self.start_point[0],self.start_point[1])
        self.parking_end_x, self.parking_end_y = self.parking_call_back(self.end_point[0],self.end_point[1])

        ######### 주차점과 가장 가까운 path 점 찾기 ########
        for i in range(len(self.global_path.x)):
            dx = self.parking_x - self.global_path.x[i]
            dy = self.parking_y - self.global_path.y[i]
            dis = sqrt(dx*dx + dy*dy)
            if dis < min_dis:
                min_dis = dis
                min_index = i

        self.parking.mindex = min_index

        self.heading = rad2deg(atan2(
            (self.global_path.y[self.parking.mindex]-self.global_path.y[self.parking.mindex - 1]), (self.global_path.x[self.parking.mindex]-self.global_path.x[self.parking.mindex - 1])))
        self.heading %= 360

        print(f"self.heading : {self.heading}")

        O3_x, O3_y, theta_O3_to_lot = self.find_O3()

        self.parking.o3x = O3_x
        self.parking.o3y = O3_y
 
        self.make_path(O3_x, O3_y, self.heading + 90, self.heading + 90-theta_O3_to_lot, self.smooth_radius, -1)

        self.parking.backward_path.x, self.parking.backward_path.y = list(reversed(self.parking.forward_path.x)), list(reversed(self.parking.forward_path.y))  

        return self.parking.forward_path, self.parking.backward_path
    
    def parking_call_back(self,x1,y1):
        x, y, _ = pymap3d.geodetic2enu(x1, y1, self.base_alt,
                                    self.base_lat, self.base_lon, self.base_alt)
        return x, y

    def find_O3(self):

        dis_mindex_to_lot = sqrt((self.parking_x - self.global_path.x[self.parking.mindex])**2 + (
            self.parking_y - self.global_path.y[self.parking.mindex])**2)
        print('dis_mindex_to_lot',dis_mindex_to_lot)
        dis_mindex_to_start = sqrt(2*dis_mindex_to_lot *
                                self.smooth_radius - dis_mindex_to_lot**2)
        print('dis_mindex_to_start',dis_mindex_to_start)
        dis_mindex_to_ego = sqrt((self.global_path.x[self.parking.mindex]-self.global_path.x[self.ego.index])
                                ** 2 + (self.global_path.y[self.parking.mindex]-self.global_path.y[self.ego.index])**2)

        dis_start_to_ego = dis_mindex_to_ego - dis_mindex_to_start

        dis_O3 = sqrt(self.smooth_radius**2 + dis_start_to_ego**2)

        theta_O3 = rad2deg(
            atan2(self.smooth_radius/dis_start_to_ego, 1))

        print('theta_O3',theta_O3)

        heading_to_O3 = self.heading - theta_O3

        theta_O3_to_lot = rad2deg(
            atan2(dis_mindex_to_start/(self.smooth_radius-dis_mindex_to_lot), 1))

        O3_x = self.global_path.x[self.ego.index] + dis_O3*cos(radians(heading_to_O3))
        O3_y = self.global_path.y[self.ego.index] + dis_O3*sin(radians(heading_to_O3))

        return O3_x, O3_y, theta_O3_to_lot      
    
    def make_path(self, x, y, start, end, radius, direction):
        start = int(round(start))
        end = int(round(end))

        # for i in range(0,30):
        #     self.parking.forward_path.x.append(self.global_path.x[self.start_index -30 +i])
        #     self.parking.forward_path.y.append(self.global_path.y[self.start_index -30 +i])

        for theta in range(start, end, direction):
            self.parking.forward_path.x.append(x+radius*cos(radians(theta)))
            self.parking.forward_path.y.append(y+radius*sin(radians(theta)))

        self.make_straight_path()

    def make_straight_path(self):
        sx,sy,ex,ey = self.parking_x, self.parking_y, self.parking_end_x, self.parking_end_y
        print('sx,sy,ex,ey',sx,sy,ex,ey)
        diff = ex- sx
        # diff = diff*10 - 10
        diff *= 10
        incline = (ey-sy)/(ex-sx)
        cnt=0
        for i in range(int(diff)):
            value = sx + i*0.1
            value_y = incline*(value-sx)+sy
                
            if cnt == 0:
                cnt = 1
                pass
            else:
                self.parking.forward_path.x.append(value)
                self.parking.forward_path.y.append(value_y)

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