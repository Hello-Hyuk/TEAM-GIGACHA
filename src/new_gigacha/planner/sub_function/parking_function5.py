import pymap3d
import json
from shared.path import Path
from math import cos, degrees, radians, sin, atan2, sqrt, hypot
from numpy import rad2deg
import csv
from .cubic_spline_planner import calc_spline_course
class Parking_Motion():
    def __init__(self, sh, pl, eg):
        self.shared = sh
        self.plan = pl
        self.ego = eg

        self.global_path = self.shared.global_path
        self.parking = self.shared.park

        #simul kcity
        # self.base_lat = 37.239231667
        # self.base_lon = 126.773156667
        # self.base_alt = 15.4

        #siheung
        self.base_lat = 37.36458356
        self.base_lon = 126.7237789
        self.base_alt = 15.4

        self.radius = 2.3
        self.o1_x = 0

        self.mapname = ''
        self.cnt = False
        # with open('/home/gigacha/TEAM-GIGACHA/src/new_gigacha/localizer/parking_KCity2.json') as pkc:
        #     self.parking_point = json.load(pkc)
        with open('/home/gigacha/TEAM-GIGACHA/src/new_gigacha/localizer/parking_siheung.json') as pkc:
            self.parking_point = json.load(pkc)


    def make_parking_tra(self):
        self.point = self.parking_point[str(self.parking.select_num)]
        # self.point = self.parking_point[str(1)]
        self.start_point = self.point["start"]
        self.end_point = self.point["end"]
        if len(self.parking.forward_path.x) == 0:
            self.findParkingPath()


    def findParkingPath(self):

        self.parking_x, self.parking_y = self.parking_call_back(self.start_point[0],self.start_point[1])
        self.parking_end_x, self.parking_end_y = self.parking_call_back(self.end_point[0],self.end_point[1])

        self.parking_width = hypot(self.parking_end_y - self.parking_y, self.parking_end_x - self.parking_x)
        self.heading = rad2deg(atan2((self.parking_end_y - self.parking_y),(self.parking_end_x - self.parking_x)))%360
        print(f"self.heading : {self.heading}")

        self.find_O1()

        O2_radius = self.find_O2()
 
        heading_O2_O1 = rad2deg(atan2(self.radius, self.parking_width))

        self.make_path(self.parking.o2x, self.parking.o2y, self.heading + 90, self.heading + 180 - heading_O2_O1 , O2_radius, 1)
        self.make_path(self.parking.o1x, self.parking.o1y, self.heading - heading_O2_O1  , self.heading - 90, self.radius, -1)
        self.make_straight_path()        

        self.parking.forward_path.x, self.parking.forward_path.y = list(reversed(self.parking.backward_path.x)), list(reversed(self.parking.backward_path.y))  

        min_index = 0
        min_dis = 10000000
        ######### 주차점과 가장 가까운 path 점 찾기 ########
        for i in range(len(self.global_path.x)):
            dx = self.parking_end_x - self.global_path.x[i]
            dy = self.parking_end_y - self.global_path.y[i]
            dis = sqrt(dx*dx + dy*dy)
            if dis < min_dis:
                min_dis = dis
                min_index = i

        self.parking.mindex = min_index + self.o1_x*10


        # return self.parking.forward_path, self.parking.backward_path
    
    def parking_call_back(self,x1,y1):
        x, y, _ = pymap3d.geodetic2enu(x1, y1, self.base_alt,
                                    self.base_lat, self.base_lon, self.base_alt)
        return x, y


    def find_O1(self):

        dis_P1_O1 = hypot(self.radius, self.o1_x)
        heading_P1_O1 = rad2deg(atan2(self.o1_x,self.radius))%360
        
        heading_O1 = (self.heading + 90 - heading_P1_O1)%360
        self.parking.o1x = self.parking_x + dis_P1_O1*cos(heading_O1)
        self.parking.o1y = self.parking_y + dis_P1_O1*sin(heading_O1)

    def find_O2(self):
        def func(a,b,c):
            return max((-b+sqrt(b**2-4*a*c))/2*a, (-b-sqrt(b**2-4*a*c))/2*a)

        O2_radius = func(1,2*self.radius,-self.parking_width**2)


        self.parking.o2x = self.parking_end_x + self.o1_x*cos(self.heading)
        self.parking.o2y = self.parking_end_y + self.o1_x*sin(self.heading)

        return O2_radius

    
    def make_path(self, x, y, start, end, radius, direction):
        start = int(round(start))
        end = int(round(end))

        # for i in range(0,30):
        #     self.parking.forward_path.x.append(self.global_path.x[self.start_index -30 +i])
        #     self.parking.forward_path.y.append(self.global_path.y[self.start_index -30 +i])

        for theta in range(start, end, direction):
            self.parking.backward_path.x.append(x+radius*cos(radians(theta)))
            self.parking.backward_path.y.append(y+radius*sin(radians(theta)))

    def make_straight_path(self):
        sx = self.parking_x + self.o1_x*cos(self.heading)
        sy = self.parking_y + self.o1_y*sin(self.heading)
        ex,ey = self.parking_x, self.parking_y
        
        x = []
        y = []
        
        x.append(sx)
        x.append(ex)
        y.append(sy)
        y.append(ey)
        
        cx, cy, _, _, _ = calc_spline_course(x, y ,ds = 0.1)
         
        self.parking.backward_path.x.extend(cx)
        self.parking.backward_path.y.extend(cy)

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
        # print(self.parking.stop_index)