#!/usr/bin/env python3
import rospy
import pymap3d
import time
from low_pass_filter import LPF
from sensor_msgs.msg import NavSatFix
from ublox_msgs.msg import NavPVT

class GPS():
    def __init__(self):
        rospy.Subscriber("ublox_gps/fix", NavSatFix, self.gps_call_back)
        rospy.Subscriber("ublox_gps/navpvt", NavPVT, self.navpvt_call_back)
        
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.time = 0.0

        self.base = rospy.get_param("Songdo_track") # KCity, Songdo, Songdo_track, Siheung
        self.lat = self.base['lat']
        self.lon = self.base['lon']
        self.alt = self.base['alt']

    def gps_call_back(self, data):
        self.x, self.y, _ = pymap3d.geodetic2enu(data.latitude, data.longitude, self.alt, \
                                            self.lat, self.lon, self.alt)

        # self.cov_x_gps = data.position_covariance[4]
        # self.cov_y_gps = data.position_covariance[0]
        # self.cov_xy_gps = data.position_covariance[1] ### for kalman filter

    def navpvt_call_back(self, data):
        self.time = time.time()
        gps_heading = (450-(data.heading * 10**(-5)))%360
        headAcc = data.headAcc
        lpf = LPF()

        if headAcc < 500000:
            self.heading = lpf.low_pass_filter(gps_heading, 30, 0.1)
        else:
            self.heading = 0.0

if __name__ == '__main__':
    try:
        gps=GPS()
    except rospy.ROSInterruptException:
        pass