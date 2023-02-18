import rospy
import pymap3d
import time
import json
from geometry_msgs.msg import Pose
from sensor_msgs.msg import NavSatFix
from ublox_msgs.msg import NavPVT

class GPS(): 
    def __init__(self, base_name): 
        rospy.Subscriber("ublox_gps/fix", NavSatFix, self.fix_call_back)
        rospy.Subscriber("ublox_gps/navpvt", NavPVT, self.navpvt_call_back)
        rospy.Subscriber("/simul_gps", Pose, self.simul_gps_call_back)

        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.hAcc = 0
        self.headAcc = 0
        self.heading_flag = True

        with open('/home/gigacha/TEAM-GIGACHA/src/new_local_pkg/base.json') as base:
            base_data = json.load(base)

        self.base = base_data[self.base_name]
        self.lat = self.base['lat']
        self.lon = self.base['lon']
        self.alt = self.base['alt']

        self.time = 0.0

    def fix_call_back(self, data):
        self.x, self.y, _ = pymap3d.geodetic2enu(data.latitude, data.longitude, data.altitude, self.lat, self.lon, self.alt)

    def simul_gps_call_back(self, data):
        self.time = time.time()
        self.x, self.y, _ = pymap3d.geodetic2enu(data.position.x, data.position.y, data.position.z, self.lat, self.lon, self.alt)

    def navpvt_call_back(self, data):
        self.time = time.time()
        self.hAcc = data.hAcc
        self.headAcc = data.headAcc
        gps_heading = (450 - (data.heading * (10 ** (-5)))) % 360

        if headAcc < 40000:
            self.heading_flag = True
            self.heading = gps_heading
        else:
            self.heading_flag = False

if __name__ == "__main__":
    try:
        gps = GPS()
    except rospy.ROSInterruptException:
        pass


