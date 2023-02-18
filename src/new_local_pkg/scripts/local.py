import rospy
import time
import argparse
from gps_new import GPS
from ahrs_new import AHRS
from odometry import DR
from local_pkg.msg import Local
from nav_msgs.msg import Path
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from local_functions_new import quaternion_from_euler as qfe
from sig_int_handler import Activate_Signal_Interrupt_Handler

class Local():
    def __init__(self, base):
        rospy.init_node("Local", anonymous = False)
        ## GLOBAL PATH SUBSCRIBER NEED

        self.pub = rospy.Publisher("/local",Local, queue_size=1)
        self.base = base 
        self.gps = GPS(self.base)
        self.imu = AHRS()
        self.dr = DR()
        self.msg = Local()
        

        self.heading = 0.0        
        self.offset = 0.0

    def heading_decision(self):
        time = time.time()

        if (time - self.gps.time) < 0.2  and (time - self.imu.time) < 0.2 :
            if self.gps.heading_flag == True :
                self.offset = self.gps.heading - self.imu.heading
                self.heading = self.imu.heading + self.offset

            else : 
                self.heading = self.imu.heading + self.offset
        else :
            self.heading = self.imu.heading + self.offset


    def main(self):
        self.heading_decision()

        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.heading = self.heading
        self.msg.roll = self.imu.roll
        self.msg.pitch = self.imu.pitch
        self.msg.hAcc = self.gps.hAcc

        self.msg.orientation.x, self.msg.orientation.y, self.msg.orientation.z, self.msg.orientation.w = qfe(self.imu.roll, self.imu.pitch, self.imu.yaw)
    

        self.pub.publish(self.msg)


if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    try : 
        loc = Local("KCity")
        rate = rospy.Rate(50)

        while not rospy.is_shutdown():
            loc.main()
            rate.sleep()

    except rospy.ROSInterruptException:
        pass