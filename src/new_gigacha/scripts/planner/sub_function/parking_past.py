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

        self.smooth_radius = 5
        self.mapname = ''
        self.cnt = False
        with open('/home/gigacha/TEAM-GIGACHA/src/new_gigacha/localizer/parking_KCity.json') as pkc:
            self.parking_point = json.load(pkc)

    def make_parking_tra(self):
        self.point = self.parking_point[str(self.parking.select_num)]
        # self.point = self.parking_point[str(1)]
        self.start_point = self.point["start"]
        self.end_point = self.point["end"]
        if len(self.parking.forward_path.x) == 0:
            self.parking.forward_path, self.parking.backward_path, self.parking.mindex = self.findParkingPath()

    # def make_parking_tra(self):
    #     self.mapname = 'park'+ str(self.parking.select_num)
    #     path1 = Path()
    #     path2 = Path()
    #     min_index = 0
    #     min_dis = 10000000

    #     with open(f"maps/kcity_parking/{self.mapname}.csv", mode="r") as csv_file:
    #         csv_reader = csv.reader(csv_file)
    #         for line in csv_reader:
    #             path1.x.append(float(line[0]))
    #             path1.y.append(float(line[1]))
    #             # self.global_path.k.append(float(line[2]))
    #             # self.global_path.yaw.append(float(line[3]))
    #     path2.x = list(reversed(path1.x))
    #     path2.y = list(reversed(path1.y))

    #     self.parking.forward_path = path1
    #     self.parking.backward_path = path2

    #     for i in range(len(self.global_path.x)-8000):
    #         dx = self.parking.forward_path.x[0] - self.global_path.x[i]
    #         dy = self.parking.forward_path.y[0] - self.global_path.y[i]
    #         dis = sqrt(dx*dx + dy*dy)
    #         if dis < min_dis:
    #             min_dis = dis
    #             min_index = i

    #     self.parking.mindex = min_index

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

        if self.parking.direction == 0:
            self.parking.stop_index = len(
                self.parking.forward_path.x)
        elif self.parking.direction == 2:
            self.parking.stop_index = len(
                self.parking.backward_path.x)

        # print('park_mindex:{}'.format(self.parking.mindex))
        # print('stop_index:{}'.format(self.parking.stop_index))
        # print('parking.index:{}'.format(self.parking.index))


    def findParkingPath(self):
        min_index = 0
        min_dis = 10000000

        self.parking_x, self.parking_y = parking_call_back(self.start_point[0],self.start_point[1])
        self.parking_end_x, self.parking_end_y = parking_call_back(self.end_point[0],self.end_point[1])

        ######### 주차점과 가장 가까운 path 점 찾기 ########
        for i in range(len(self.global_path.x)-8000):
            dx = self.parking_x - self.global_path.x[i]
            dy = self.parking_y - self.global_path.y[i]
            dis = sqrt(dx*dx + dy*dy)
            if dis < min_dis:
                min_dis = dis
                min_index = i
        self.parking.mindex = min_index

        self.heading = rad2deg(atan2(
            (self.global_path.y[self.parking.mindex]-self.global_path.y[self.parking.mindex - 1]), (self.global_path.x[self.parking.mindex]-self.global_path.x[self.parking.mindex - 1])))
        
        print(f"min_inex : {self.parking.mindex}")
        print(f"yaw : {self.heading}")

        ######### O2, O1 원점 찾기 ########직각주차##############################################
        # O2_x, O2_y = find_O2(path, ego, min_index) # 직각주차
        # O1_x, O1_y, heading_O1_02, dis_O1_to_lot = find_O1(
        #     path, ego, min_index, parking_lot) # 직각주차
        
        ######### 전진 원호 생성 ########
        # self.parking.forward_path = make_arc_path(
        #     O2_x, O2_y, heading - 90, heading, minimum_radius, forward_path, 1)  # 직각주차

        ######### 후진 원호 생성 ########
        # O2_back_arc_heading = heading - (90 - heading_O1_02) # 직각주차
        # self.parking.backward_path = make_arc_path(
        #     O2_x, O2_y, heading, O2_back_arc_heading, minimum_radius, backward_path, -1) # 직각주차
        # self.parking.backward_path = make_arc_path(
        #     O1_x, O1_y, O2_back_arc_heading+180, heading + 180, dis_O1_to_lot, backward_path, 1)  # 직각주차
        ########################################################################################

        ########### smooth #############
        O3_x, O3_y, theta_O3_to_lot, dis_mindex_to_start = self.find_O3()  

        self.start_index = min_index - int(dis_mindex_to_start*10)
        self.make_path(O3_x, O3_y, self.heading + 90, self.heading + 90-theta_O3_to_lot, self.smooth_radius, -1)

        self.parking.backward_path.x, self.parking.backward_path.y = list(reversed(self.parking.forward_path.x)), list(reversed(self.parking.forward_path.y))  

        print('self.start_index: ',self.start_index)
        print("Parking_path Created")

        return self.parking.forward_path, self.parking.backward_path, self.start_index

    def find_O3(self):

        dis_mindex_to_lot = sqrt((self.parking_x - self.global_path.y[self.parking.mindex])**2 + (
            self.parking_y - self.global_path.y[self.parking.mindex])**2)
        dis_mindex_to_start = sqrt(2*dis_mindex_to_lot *
                                self.smooth_radius - dis_mindex_to_lot**2)
        dis_mindex_to_ego = sqrt((self.global_path.x[self.parking.mindex]-self.global_path.x[self.ego.index])
                                ** 2 + (self.global_path.y[self.parking.mindex]-self.global_path.y[self.ego.index])**2)
        dis_start_to_ego = dis_mindex_to_ego - dis_mindex_to_start
        dis_O3 = sqrt(self.smooth_radius**2 + dis_start_to_ego**2)

        theta_O3 = rad2deg(
            atan2(self.smooth_radius/dis_start_to_ego, 1))
        heading_to_O3 = self.heading - theta_O3

        theta_O3_to_lot = rad2deg(
            atan2(dis_mindex_to_start/(self.smooth_radius-dis_mindex_to_lot), 1))

        O3_x = self.global_path.x[self.ego.index] + dis_O3*cos(radians(heading_to_O3))
        O3_y = self.global_path.y[self.ego.index] + dis_O3*sin(radians(heading_to_O3))

        return O3_x, O3_y, theta_O3_to_lot, dis_mindex_to_start        
    
    def make_path(self, x, y, start, end, radius, direction):
        start = int(round(start))
        end = int(round(end))

        for i in range(0,30):
            self.parking.forward_path.x.append(self.global_path.x[self.start_index -30 +i])
            self.parking.forward_path.y.append(self.global_path.y[self.start_index -30 +i])

        for theta in range(start, end, direction):
            self.parking.forward_path.x.append(x+radius*cos(radians(theta)))
            self.parking.forward_path.y.append(y+radius*sin(radians(theta)))

        # self.make_straight_path()

    def make_straight_path(self):
        sx,sy,ex,ey = self.parking_x, self.parking_y, self.parking_end_x, self.parking_end_y
        print('sx,sy,ex,ey',sx,sy,ex,ey)
        diff = ex- sx
        diff = diff*10 - 20
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



















############################################################################
#####              ↓↓↓↓ parking path create function ↓↓↓↓               ####
############################################################################



# 여기서 parking_lot은 주차 구역 입구 정중앙을 뜻함.

WB = 1.04
max_angle = 27
kingpin_r = 0.05
minimum_radius = WB/sin(radians(max_angle)) + kingpin_r
smooth_radius = 5

def find_O2(path, ego, min_index):

    # distance_from_min_index
    dis_mindex = sqrt((path.x[ego.index] - path.x[min_index])
                      ** 2 + (path.y[ego.index] - path.y[min_index])**2)  # 차량과  주차점 가장 근처 path 사이 직선 거리

    dis_O2 = sqrt((dis_mindex)**2 + minimum_radius**2)  # O2와 차량 사이 거리

    theta_O2_mindex = rad2deg(atan2(minimum_radius / dis_mindex, 1.0))
    heading_to_O2 = heading + theta_O2_mindex  # heading 음수일 때는 달라짐

    O2_x = path.x[ego.index] + dis_O2*cos(radians(heading_to_O2))
    O2_y = path.y[ego.index] + dis_O2*sin(radians(heading_to_O2))

    return O2_x, O2_y


def find_O1(path, ego, min_index, parking_lot):

    dis_mindex_to_lot = sqrt((parking_lot['x'] - path.x[min_index])**2 + (
        parking_lot['y'] - path.y[min_index])**2)  # mindex와 parking_lot 사이 거리

    dis_O1_to_lot = dis_mindex_to_lot * \
        (1+dis_mindex_to_lot/(2*minimum_radius))  # O1과 parking_lot사이 수직 거리

    O1_x = parking_lot['x'] + dis_O1_to_lot*cos(radians(heading))
    O1_y = parking_lot['y'] + dis_O1_to_lot*sin(radians(heading))

    theta_O1_to_O2 = rad2deg(atan2(
        dis_O1_to_lot / (dis_mindex_to_lot + minimum_radius), 1.0))

    return O1_x, O1_y, theta_O1_to_O2, dis_O1_to_lot





def make_arc_path(x, y, start, end, radius, path, direction):
    start = int(round(start))
    end = int(round(end))

    for theta in range(start, end, direction):
        path.x.append(x+radius*cos(radians(theta)))
        path.y.append(y+radius*sin(radians(theta)))

    return path

def make_straight_path(sx,sy,ex,ey):
    diff = ex- sx
    diff = diff*10
    path= Path()
    for i in range(int(diff)):
        value = sx + i*0.1
        value_y=((ey-sy)/(ex-sx))(value-sx)+sy

        path.x.append(value)
        path.y.append(value_y)

    return path

    

# Songdo
# base_lat = 37.3843177
# base_lon = 126.6553022
# base_alt = 15.4

# simul_kcity_sangwook
# base_lat = 37.2389871166175
# base_lon = 126.772996046328
# base_alt = 15.4

#simul kcity
base_lat = 37.239231667
base_lon = 126.773156667
base_alt = 15.4
# Songdo ParkingLot
# parking_lat = 37.3848150059503
# parking_lon = 126.655830146935

# simul_kcity_sangwook ParkingLot_vertical
parking_lat = 37.2392303963579
parking_lon = 126.773196841119

# simul_kcity_sangwook ParkingLot_smooth
# parking_lat = 37.239270000000005
# parking_lon = 126.77322666666666

# parking_lat = 37.2392083231717
# parking_lon = 126.773241462183


def parking_call_back(x1,y1):
    x, y, _ = pymap3d.geodetic2enu(x1, y1, base_alt,
                                   base_lat, base_lon, base_alt)
    return x, y