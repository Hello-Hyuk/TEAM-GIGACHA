import pymap3d
import json
from shared.path import Path
from math import cos, degrees, radians, sin, atan2, sqrt, hypot
from numpy import rad2deg

class Parking_Motion():
    def __init__(self, sh, pl, eg):
        self.shared = sh
        self.plan = pl
        self.ego = eg

        self.global_path = self.shared.global_path
        self.parking = self.shared.park

        with open('/home/gigacha/TEAM-GIGACHA/src/new_gigacha/localizer/parking_KCity.json') as pkc:
            self.parking_point = json.load(pkc)

    def make_parking_tra(self):
        self.point = self.parking_point[self.parking.select_num]
        start_point = self.point["start"]
        end_point = self.point["end"]
        x = start_point[0]
        y = start_point[1]
        if len(self.parking.forward_path.x) == 0:
            self.parking.forward_path, self.parking.backward_path, self.parking.mindex = findParkingPath(
                self.ego, self.global_path, start_point, end_point)

    def park_index_finder(self):
        min_dis = -1
        min_idx = 0
        step_size = 10
        save_idx = 0

        for i in range(max(self.parking.index - step_size, 0), self.parking.index + step_size):
            try:
                dis = hypot(
                    self.parking.forward_path.x[i] - self.ego.x, self.parking.forward_path.y[i] - self.ego.y)
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
        self.parking.index = self.park_index_finder()

        if self.parking.direction == 0:
            self.parking.stop_index = len(
                self.parking.forward_path.x)
        elif self.parking.direction == 2:
            self.parking.stop_index = len(
                self.parking.backward_path.x)

        print(self.parking.direction)
        # print('park_mindex:{}'.format(self.parking.mindex))
        # print('stop_index:{}'.format(self.parking.stop_index))
        # print('parking.index:{}'.format(self.parking.index))


############################################################################
#####              ↓↓↓↓ parking path create function ↓↓↓↓               ####
############################################################################

WB = 1.04
max_angle = 27
kingpin_r = 0.05
minimum_radius = WB/sin(radians(max_angle)) + kingpin_r
smooth_radius = 5

# 여기서 parking_lot은 주차 구역 입구 정중앙을 뜻함.


    def findParkingPath(ego, path, start_point, end_point):
        global heading
        min_index = 0
        min_dis = 10000000
        forward_path = Path()
        backward_path = Path()
        straight_path = Path()

        parking_x, parking_y = parking_call_back(start_point[0],start_point[1])
        parking_end_x, parking_end_y = parking_call_back(end_point[0],end_point[1])


        parking_lot = {
            'x': parking_x,
            'y': parking_y
        }

        ######### 주차점과 가장 가까운 path 점 찾기 ########
        for i in range(len(path.x)-13000):
            dx = parking_lot['x'] - path.x[i]
            dy = parking_lot['y'] - path.y[i]
            dis = sqrt(dx*dx + dy*dy)
            if dis < min_dis:
                min_dis = dis
                min_index = i
        print(f"min_inex : {min_index}")
        heading = rad2deg(atan2(
            (path.y[min_index]-path.y[min_index - 1]), (path.x[min_index]-path.x[min_index - 1])))
        print(f"yaw : {heading}")

        ######### O2, O1 원점 찾기 ########
        # O2_x, O2_y = find_O2(path, ego, min_index) # 직각주차
        # O1_x, O1_y, heading_O1_02, dis_O1_to_lot = find_O1(
        #     path, ego, min_index, parking_lot) # 직각주차
        
        ######### 전진 원호 생성 ########
        # forward_path = make_arc_path(
        #     O2_x, O2_y, heading - 90, heading, minimum_radius, forward_path, 1)  # 직각주차

        ######### 후진 원호 생성 ########
        # O2_back_arc_heading = heading - (90 - heading_O1_02) # 직각주차
        # backward_path = make_arc_path(
        #     O2_x, O2_y, heading, O2_back_arc_heading, minimum_radius, backward_path, -1) # 직각주차
        # backward_path = make_arc_path(
        #     O1_x, O1_y, O2_back_arc_heading+180, heading + 180, dis_O1_to_lot, backward_path, 1)  # 직각주차

        ########### smooth #############
        O3_x, O3_y, theta_O3_to_lot, dis_mindex_to_start = find_O3(
            path, ego, min_index, parking_lot, heading)  

        forward_path = make_arc_path(O3_x, O3_y, heading + 90, heading +
                                    90-theta_O3_to_lot, smooth_radius, forward_path, -1)
        straight_path = make_straight_path(parking_x, parking_y,parking_end_x, parking_end_y)
        backward_path.x, backward_path.y = forward_path.x.reverse(
        ), forward_path.y.reverse()  
        print('dis_mindex_to_start',dis_mindex_to_start)
        min_index = min_index - int(dis_mindex_to_start*10)
        print('111',min_index)
        print("Parking_path Created")

        return forward_path, backward_path, min_index


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


def find_O3(path, ego, min_index, parking_lot, heading):

    dis_mindex_to_lot = sqrt((parking_lot['x'] - path.x[min_index])**2 + (
        parking_lot['y'] - path.y[min_index])**2)
    dis_mindex_to_start = sqrt(2*dis_mindex_to_lot *
                               smooth_radius - dis_mindex_to_lot**2)
    dis_mindex_to_ego = sqrt((path.x[min_index]-path.x[ego.index])
                             ** 2 + (path.y[min_index]-path.y[ego.index])**2)
    dis_start_to_ego = dis_mindex_to_ego - dis_mindex_to_start
    dis_O3 = sqrt(smooth_radius**2 + dis_start_to_ego**2)

    theta_O3 = rad2deg(
        atan2(smooth_radius/dis_start_to_ego, 1))
    heading_to_O3 = heading - theta_O3

    theta_O3_to_lot = rad2deg(
        atan2(dis_mindex_to_start/(smooth_radius-dis_mindex_to_lot), 1))

    O3_x = path.x[ego.index] + dis_O3*cos(radians(heading_to_O3))
    O3_y = path.y[ego.index] + dis_O3*sin(radians(heading_to_O3))

    return O3_x, O3_y, theta_O3_to_lot, dis_mindex_to_start


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