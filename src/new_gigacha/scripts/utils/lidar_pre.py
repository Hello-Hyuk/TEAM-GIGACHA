#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
from sensor_msgs.msg import ChannelFloat32
import pcl
import struct
import ctypes
import numpy as np

def pcl_to_ros(pcl_array):
    """ Converts a pcl PointXYZRGB to a ROS PointCloud2 message
    
        Args:
            pcl_array (PointCloud_PointXYZRGB): A PCL XYZRGB point cloud
            
        Returns:
            PointCloud2: A ROS point cloud
    """
    ros_msg = PointCloud2()

    ros_msg.header.stamp = rospy.Time.now()
    ros_msg.header.frame_id = "velodyne"

    ros_msg.height = 1
    ros_msg.width = pcl_array.size

    ros_msg.fields.append(PointField(
                            name="x",
                            offset=0,
                            datatype=PointField.FLOAT32, count=1))
    ros_msg.fields.append(PointField(
                            name="y",
                            offset=4,
                            datatype=PointField.FLOAT32, count=1))
    ros_msg.fields.append(PointField(
                            name="z",
                            offset=8,
                            datatype=PointField.FLOAT32, count=1))
    ros_msg.fields.append(PointField(
                            name="rgb",
                            offset=16,
                            datatype=PointField.FLOAT32, count=1))

    ros_msg.is_bigendian = False
    ros_msg.point_step = 32
    ros_msg.row_step = ros_msg.point_step * ros_msg.width * ros_msg.height
    ros_msg.is_dense = False
    buffer = []

    for data in pcl_array:
        s = struct.pack('>f', data[3])
        i = struct.unpack('>l', s)[0]
        pack = ctypes.c_uint32(i).value

        r = (pack & 0x00FF0000) >> 16
        g = (pack & 0x0000FF00) >> 8
        b = (pack & 0x000000FF)

        buffer.append(struct.pack('ffffBBBBIII', data[0], data[1], data[2], 1.0, b, g, r, 0, 0, 0, 0))

    ros_msg.data = b"".join(buffer)

    return ros_msg

def getMsg_lidar(msg):
    gen = point_cloud2.read_points(msg, skip_nans=True)
    cnt = 0
    points_list = []

    for p in gen:
        points_list.append([p[0] + 1.05, p[1], p[2], p[3]])
        
    pcl_data = pcl.PointCloud_PointXYZRGB()
    pcl_data.from_list(points_list)
    cloud_new = pcl_to_ros(pcl_data)
    pub.publish(cloud_new)
    
    
    
rospy.init_node("lidar", anonymous=True)
pub = rospy.Publisher("lidar_pub", PointCloud2, queue_size=1)
rospy.Subscriber("/velodyne_points", PointCloud2, getMsg_lidar)

rospy.spin()
rate = rospy.Rate(20) 
rate.sleep()