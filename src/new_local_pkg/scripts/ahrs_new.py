import numpy as np
import rospy
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Imu
import time
from local_functions_new import euler_from_quaternion as efq


class AHRS():
    def __init__(self):
        rospy.init_node('ahrs', anonymous = False)
        rospy.Subscriber("/imu", Imu, self.Imu_callback)
        rospy.Subscriber("/simul_imu", Pose, self.simul_Imu_callback)
        self.heading = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

        self.time = 0.0
        self.battery = 0.0

        self.data_q = Quaternion()

        

    def Imu_callback(self,data):
        self.time = time.time()
        self.data_q = data.orientation
        self.roll, self.pitch, self.yaw = efq(self.data_q.x, self.data_q.y, self.data_q.z, self.data_q.w)

        self.heading = np.rad2deg(-1*self.yaw)%360
        print("heading : ", self.heading)
        self.battery = data.linear_acceleration.z


    def simul_Imu_callback(self,data):
        self.time = time.time()
        self.data_q = data.orientation
        self.roll, self.pitch, self.yaw = efq(self.data_q.x, self.data_q.y, self.data_q.z, self.data_q.w)

        self.heading = np.rad2deg(self.yaw)%360

if __name__ == "__main__" :
    try : 
        imu = AHRS()
        rospy.spin()

    except rospy.ROSInterruptException :
        pass