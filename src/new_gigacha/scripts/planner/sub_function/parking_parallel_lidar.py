#!/usr/bin/env python3 

import pymap3d
import rospy 
import json

from time import sleep, time
from math import cos, sin, pi 

from sensor_msgs import point_cloud2 
from sensor_msgs.msg import PointCloud2 
from sensor_msgs.msg import PointField 
from sensor_msgs.msg import PointCloud 
from sensor_msgs.msg import ChannelFloat32 
from geometry_msgs.msg import Point32 
from std_msgs.msg import Int32, String 
from nav_msgs.msg import Odometry
 
import numpy as np 
from shapely.geometry import Point, Polygon 

class PL():
    def __init__(self, ego):

        self.ego = ego
        rospy.Subscriber("/velodyne_points", PointCloud2, self.getMsg_parking) 
        self.pub = rospy.Publisher("lidar_pub", PointCloud, queue_size=1) 
        self.pub_num = rospy.Publisher("Parking_num", Int32, queue_size=1) 

        # simul kcity
        self.base_lat = 37.23873
        self.base_lon = 126.772383333333
        self.base_alt = 15.4
        with open('/home/gigacha/TEAM-GIGACHA/src/new_gigacha/scripts/planner/sub_function/parking_JSON/parking_KCity_parallel_roi.json') as pkc:
            self.parking_point = json.load(pkc)

    def parking(self, temp_points):
        parking_point_x_y = []

        for i in range(1, 6):
            self.point = self.parking_point[str(i)]
            for j in range(1, 5):
                x1 = self.point[str(j)][0]
                y1 = self.point[str(j)][1]
                x, y, _ = pymap3d.geodetic2enu(x1, y1, self.base_alt, self.base_lat, self.base_lon, self.base_alt)
                parking_point_x_y.append([x, y])

        parking_space_1 = [parking_point_x_y[0], parking_point_x_y[1], parking_point_x_y[2], parking_point_x_y[3]] 
        parking_space_2 = [parking_point_x_y[4], parking_point_x_y[5], parking_point_x_y[6], parking_point_x_y[7]] 
        parking_space_3 = [parking_point_x_y[8], parking_point_x_y[9], parking_point_x_y[10], parking_point_x_y[11]] 
        parking_space_4 = [parking_point_x_y[12], parking_point_x_y[13], parking_point_x_y[14], parking_point_x_y[15]] 
        parking_space_5 = [parking_point_x_y[16], parking_point_x_y[16], parking_point_x_y[18], parking_point_x_y[19]]

        # 직사각형 생성 
        parking_space_poly1 = Polygon(parking_space_1) 
        parking_space_poly2 = Polygon(parking_space_2) 
        parking_space_poly3 = Polygon(parking_space_3) 
        parking_space_poly4 = Polygon(parking_space_4) 
        parking_space_poly5 = Polygon(parking_space_5)
    
        parking_result = [0, 0, 0, 0, 0] 
        
        for i in range(len(temp_points)): 
            test_code = Point(temp_points[i].x, temp_points[i].y) 
            if test_code.within(parking_space_poly1): 
                parking_result[0]+=1 
            if test_code.within(parking_space_poly2): 
                parking_result[1]+=1 
            if test_code.within(parking_space_poly3): 
                parking_result[2]+=1 
            if test_code.within(parking_space_poly4): 
                parking_result[3]+=1 
            if test_code.within(parking_space_poly5): 
                parking_result[4]+=1 
    
        # print("parking 1 :", parking_result[0])  
        # print("parking 2 :", parking_result[1]) 
        # print("parking 3 :", parking_result[2]) 
        # print("parking 4 :", parking_result[3]) 
        # print("parking 5 :", parking_result[4]) 
        # print("parking 6 :", parking_result[5]) 
        
        result_number = -1

        # parallel
        if 9530 < self.ego.index < 9560:
            for i in range(0, 2): 
                if parking_result[i] < 5: 
                    result_number = i + 1 
                    break
        elif 9700 < self.ego.index < 9730:
            if parking_result[2] < 5: 
                result_number = i + 1
        else:
            for i in range(4, 6): 
                if parking_result[i] < 5: 
                    result_number = i + 1
                    break
        
        return result_number
 
    def getMsg_parking(self, lidar_data): 
        gen = point_cloud2.read_points(lidar_data, skip_nans=True) 
        cnt = 0 
        points_list = [] 
    
        for p in gen: 
            if (0 < p[0] < 20) and (-15 < p[1] < 0) and (-0.6 < p[2]): 
                points_list.append([p[0] + 1.15, p[1], p[2], p[3]]) 
    
        test = PointCloud() 
        get_in = ChannelFloat32() 
        get_in.name = 'VLP_intensery' 
        test.points = [] 
        theta = self.ego.heading * pi / 180 
        for p in points_list: 
            park = Point32() 
            park.x = p[0] * cos(theta) + p[1] * -sin(theta) + self.ego.x
            park.y = p[0] * sin(theta) + p[1] * cos(theta) + self.ego.y
            park.z = 0 
            get_in.values.append(p[3]) 
            test.points.append(park) 
            cnt += 1 
    
        parking_number = Int32() 
        parking_number.data = self.parking(test.points) 
        self.pub_num.publish(parking_number) 
        # print('===================================================parking number published', parking_number) 
        test.channels.append(get_in) 
        test.header.frame_id = 'map' 
        test.header.stamp = rospy.Time.now() 
        self.pub.publish(test)