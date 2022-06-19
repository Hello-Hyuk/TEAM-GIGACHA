#!/usr/bin/env python3
import rospy
import numpy as np
import time

from lib.local_utils.euler_from_quaternion import euler_from_quaternion as efq
from sensor_msgs.msg import Imu

class IMU():
    def __init__(self):
        self.heading = 0.0
        self.battery = 0
        self.time = 0.0
        
        rospy.Subscriber("/imu", Imu, self.imu_call_back)

        imu = Imu()
        # self.orientation_q = imu.orientation

    def imu_call_back(self, data):
        self.time = time.time()
        orientation_q = data.orientation
        roll, pitch, yaw = efq(orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w)

        self.heading = np.rad2deg(-1*yaw)%360
        self.battery = data.angular_velocity.x

if __name__ == '__main__':
    try:
        imu=IMU()
    except rospy.ROSInterruptException:
        pass