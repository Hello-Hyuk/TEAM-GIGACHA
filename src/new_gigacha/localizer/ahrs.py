#!/usr/bin/env python3
import rospy
import numpy as np
import time
from geometry_msgs.msg import Pose
from localizer.local_functions import euler_from_quaternion as efq
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion

class IMU():
    def __init__(self):
        self.heading = 0.0
        self.battery = 0
        self.time = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        
        rospy.Subscriber("/imu", Imu, self.imu_call_back)
        rospy.Subscriber("/simul_imu", Pose, self.imu_call_back)

        self.orientation_q = Quaternion()

    def imu_call_back(self, data):
        self.time = time.time()
        self.orientation_q = data.orientation
        roll, pitch, yaw = efq(self.orientation_q.x, self.orientation_q.y, self.orientation_q.z, self.orientation_q.w)
        
        self.roll = roll
        self.pitch = pitch

        self.heading = np.rad2deg(-1*yaw)%360 # real world
        self.battery = data.angular_velocity.x
        # self.heading = np.rad2deg(yaw)%360 # simul


if __name__ == '__main__':
    try:
        imu=IMU()
    except rospy.ROSInterruptException:
        pass