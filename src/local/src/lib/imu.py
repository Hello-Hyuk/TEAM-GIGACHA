#!/usr/bin/env python3
import rospy
import numpy as np

from lib.euler_from_quaternion import euler_from_quaternion as efq
from lib.low_pass_filter import LPF
from sensor_msgs.msg import Imu


class IMU():
    def __init__(self):
        self.yaw = 0
        self.yaw_rate = 0
        self.lpf = LPF()

        rospy.Subscriber("/imu", Imu, self.imu_call_back)

    def imu_call_back(self, data):
        self.vis_msg.pose.orientation = data.orientation
        self.yaw_rate = -data.angular_velocity.z

        orientation_q = data.orientation
        roll, pitch, yaw = efq(orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)

        yaw = np.rad2deg(yaw)

        self.yaw = self.lpf.low_pass_filter(yaw, 100, 0.2) # data, size, alpha

if __name__ == '__main__':
    try:
        imu=IMU()
    except rospy.ROSInterruptException:
        pass