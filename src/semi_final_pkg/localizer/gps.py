#!/usr/bin/env python3
import rospy
import pymap3d
import time
from geometry_msgs.msg import Pose
from sensor_msgs.msg import NavSatFix
from ublox_msgs.msg import NavPVT

class GPS():
    def __init__(self):
        rospy.Subscriber("ublox_gps/fix", NavSatFix, self.gps_call_back)
        rospy.Subscriber("ublox_gps/navpvt", NavPVT, self.navpvt_call_back)
        rospy.Subscriber("/simul_gps", Pose, self.gps_call_back_simul)
        
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.heading_switch = False

        self.time = 0.0
        self.init = False

        self.lat = 0.0
        self.lon = 0.0
        self.alt = 0.0

    def gps_call_back(self, data):
        if self.init == False:
            self.lat = data.latitude
            self.lon = data.longitude
            self.alt = 15.4
            self.init = True
        else:
            self.x, self.y, _ = pymap3d.geodetic2enu(data.latitude, data.longitude, self.alt, \
                                                self.lat, self.lon, self.alt)

    # def gps_call_back(self, data):
    #     self.lat = data.latitude
    #     self.lon = data.longitude

    def gps_call_back_simul(self, data):
        if self.init == False:
            self.lat = data.latitude
            self.lon = data.longitude
            self.alt = 15.4
            self.init = True
        else:
            self.x, self.y, _ = pymap3d.geodetic2enu(data.position.x, data.position.y, self.alt, \
                                        self.lat , self.lon, self.alt)
        self.time = time.time()

    def navpvt_call_back(self, data):
        self.time = time.time()
        gps_heading = (450-(data.heading * 10**(-5)))%360
        headAcc = data.headAcc
        
        if headAcc < 600000:
            self.heading_switch = True
            self.heading = gps_heading
        else:
            self.heading_switch = False
            self.heading = 0.0

if __name__ == '__main__':
    try:
        gps=GPS()
    except rospy.ROSInterruptException:
        pass