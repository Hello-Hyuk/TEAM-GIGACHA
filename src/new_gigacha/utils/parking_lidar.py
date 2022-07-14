#!/usr/bin/env python3

import rospy
import pymap3d
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
from sensor_msgs.msg import ChannelFloat32

import numpy as np
from nav_msgs.msg import Odometry
from math import cos, sin, pi
from shapely.geometry import Point, Polygon
from std_msgs.msg import Int32, String

global lidar_temp, lidar_cur_state
global yaw, cur_x, cur_y
lidar_temp = PointCloud2()
lidar_cur_state = 'parking-base1'

def parking(temp_points):
    parking_point_x_y = [[9.021042, 9.433509],[8.873212, 12.023061],[10.647854, 12.023063],[10.352018, 14.612615],[11.978832, 14.612617],[11.830912, 17.202281],[13.309809, 17.202283],[13.161889, 19.791835],[14.640786, 19.791837],[14.492865, 22.381390],[15.971761, 22.566400],[15.823840, 24.971055],[20.709098, 25.340970],[20.556188, 22.751418],[19.225208, 22.751414],[19.373130, 20.161751],[17.894234, 20.161748],[17.894239, 17.572196],[16.563259, 17.387185],[16.563263, 14.982641],[15.084455, 14.797630],[15.232287, 12.392975],[13.753477, 12.392972],[13.901309, 9.803420]]

    parking_space_1 = [parking_point_x_y[0], parking_point_x_y[1], parking_point_x_y[22], parking_point_x_y[23]]
    parking_space_2 = [parking_point_x_y[1], parking_point_x_y[3], parking_point_x_y[20], parking_point_x_y[21]]
    parking_space_3 = [parking_point_x_y[3], parking_point_x_y[5], parking_point_x_y[18], parking_point_x_y[19]]
    parking_space_4 = [parking_point_x_y[5], parking_point_x_y[7], parking_point_x_y[16], parking_point_x_y[17]]
    parking_space_5 = [parking_point_x_y[7], parking_point_x_y[9], parking_point_x_y[14], parking_point_x_y[15]]
    parking_space_6 = [parking_point_x_y[9], parking_point_x_y[11], parking_point_x_y[12], parking_point_x_y[13]]

    # 직사각형 생성
    parking_space_poly1 = Polygon(parking_space_1)
    parking_space_poly2 = Polygon(parking_space_2)
    parking_space_poly3 = Polygon(parking_space_3)
    parking_space_poly4 = Polygon(parking_space_4)
    parking_space_poly5 = Polygon(parking_space_5)
    parking_space_poly6 = Polygon(parking_space_6)

    parking_result = [0, 0, 0, 0, 0, 0]
    
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
        if test_code.within(parking_space_poly6):
            parking_result[5]+=1

    print("parking 1 :", parking_result[0]) 
    print("parking 2 :", parking_result[1])
    print("parking 3 :", parking_result[2])
    print("parking 4 :", parking_result[3])
    print("parking 5 :", parking_result[4])
    print("parking 6 :", parking_result[5])
    
    result_number = -1

    for i in range(0, 6):
        if parking_result[i] < 5:
            result_number = i + 1
            return result_number

    # elif lidar_cur_state == 'parking-base2':
    #     for i in range(3, 6):
    #         if parking_result[i] < 5:
    #             result_number = i + 1
    #             return result_number
    
    # return result_number

def pose_callback(msg):
    global yaw, cur_x, cur_y
    
    cur_x = msg.pose.pose.position.x
    cur_y = msg.pose.pose.position.y
    yaw = msg.pose.pose.position.z

def getMsg_parking(lidar_data):
    # global yaw, cur_x, cur_y

    gen = point_cloud2.read_points(lidar_data, skip_nans=True)
    cnt = 0
    points_list = []

    for p in gen:
        if 0 < p[0] < 20:
            if 0 < p[1] < 10:
                points_list.append([p[0] + 0.5, p[1], p[2], p[3]])

    test = PointCloud()
    get_in = ChannelFloat32()
    get_in.name = 'VLP_intensery'
    test.points = []
    theta = (yaw) * pi / 180
    for p in points_list:
        park = Point32()
        park.x = p[0] * cos(theta) + p[1] * -sin(theta) + cur_x
        park.y = p[0] * sin(theta) + p[1] * cos(theta) + cur_y
        park.z = 0
        get_in.values.append(p[3])
        test.points.append(park)
        cnt += 1

    parking_number = Int32()
    # print(type(test.points))
    parking_number.data = parking(test.points)
    pub_num.publish(parking_number)
    print('===================================================parking number published', parking_number)

    #print("Input :", cnt)
    test.channels.append(get_in)
    test.header.frame_id = 'map'
    test.header.stamp = rospy.Time.now()
    pub.publish(test)


rospy.init_node("lidar", anonymous=True)
pub = rospy.Publisher("lidar_pub", PointCloud, queue_size=1)
pub_num = rospy.Publisher("Parking_num", Int32, queue_size=1)
rospy.Subscriber("/vis_position", Odometry, pose_callback)
rospy.Subscriber("/velodyne_points", PointCloud2, getMsg_parking)

rate = rospy.Rate(20)  # 100hz
rate.sleep()
rospy.spin()
