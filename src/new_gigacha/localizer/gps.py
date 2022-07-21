#!/usr/bin/env python3
import rospy
import pymap3d
import time
import json
from geometry_msgs.msg import Pose
# from localizer.local_functions import LPF
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

        with open('/home/gigacha/TEAM-GIGACHA/src/new_gigacha/localizer/base.json') as base:
            base_data = json.load(base)

        self.base = base_data["Yonghyeon_parking"] # KCity, Songdo, Songdo_track, Siheung, KCity2, Yonghyeon_parking
        self.lat = self.base['lat']
        self.lon = self.base['lon']
        self.alt = self.base['alt']

    def gps_call_back(self, data):
        self.x, self.y, _ = pymap3d.geodetic2enu(data.latitude, data.longitude, self.alt, \
                                            self.lat, self.lon, self.alt)

    def gps_call_back_simul(self, data):
        self.x, self.y, _ = pymap3d.geodetic2enu(data.position.x, data.position.y, self.alt, \
                                    self.lat , self.lon, self.alt)
        self.time = time.time()


    def navpvt_call_back(self, data):
        self.time = time.time()
        gps_heading = (450-(data.heading * 10**(-5)))%360
        headAcc = data.headAcc
        # lpf = LPF()

        if headAcc < 600000:
            self.heading_switch = True
            self.heading = gps_heading
        else:
            self.heading_switch = False
            # self.heading = 0.0

if __name__ == '__main__':
    try:
        gps=GPS()
    except rospy.ROSInterruptException:
        pass