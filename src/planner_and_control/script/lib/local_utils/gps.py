#!/usr/bin/env python3
import rospy
import pymap3d

from gps_parse import GNGGA_Parsing


class GPS():
    def __init__(self):
        self.gngga = GNGGA_Parsing()

        self.x = 0
        self.y = 0
        self.yaw_gps = 0

        # KCity
        self.lat_origin = 37.239231667
        self.lon_origin = 126.773156667
        self.alt_origin = 15.400
        
        # #Songdo
        # self.lat_origin = 37.3851693 
        # self.lon_origin = 126.6562271
        # self.alt_origin = 15.4


    def gps_call_back(self):
        self.x, self.y, _ = pymap3d.geodetic2enu(self.gngga.lat, self.gngga.lon, self.alt_origin, \
                                            self.lat_origin , self.lon_origin, self.alt_origin)

        # self.cov_x_gps = data.position_covariance[4]
        # self.cov_y_gps = data.position_covariance[0]
        # self.cov_xy_gps = data.position_covariance[1] ### for kalman filter

if __name__ == '__main__':
    try:
        gps=GPS()
    except rospy.ROSInterruptException:
        pass