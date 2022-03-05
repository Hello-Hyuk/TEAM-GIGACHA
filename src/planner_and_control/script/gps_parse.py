#!/usr/bin/env python3
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from sensor_msgs.msg import NavSatFix

import serial
import rospy
import threading

class GPRMC_Parsing:
    def __init__(self):
        self.ser = serial.Serial('/dev/gps', baudrate = 115200, timeout = 0.5)
        print('GPRMC_Parsing : Serial connecting to /dev/gps')

        rospy.init_node("GPRMC_Parsing", anonymous = True)
        self.pub = rospy.Publisher("/GPRMC", NavSatFix, queue_size = 1)
        print("GPRMC_Parsing : Initializing ROS node...")

        self.gprmc_msg = NavSatFix()
        self.gprmc_msg.header.stamp = rospy.Time.now()
        self.gprmc_msg.header.frame_id = "gps"

    def parese_gprmc(self):
        data = self.ser.readline()

        if data[0:6] == "$GPRMC":
            sdata = data.split(",")
            
            if sdata[2] == "V":
                print("GPRMC_Parsing : No satellite data available")
                return
            print("==========Parsing GPRMC==========")
            status = sdata[2] # A : Good, V : Bad
            lat = self.decode(sdata[3])
            dirLat = sdata[4]
            lon = self.decode(sdata[5])
            dirLon = sdata[6]
            speed = 1.8 * sdata[7]
            heading = sdata[8]

            self.gprmc_msg.latitude = lat
            self.gprmc_msg.longitude = lon
            self.gprmc_msg.altitude = heading # gps heading

            if status == "A":
                self.gprmc_msg.status.status = 1
            else:
                self.gprmc_msg.status.status = -1
            
            self.pub.publish(self.gprmc_msg)

    def decode(self, coord):
        x = coord.split(".")
        head = x[0]
        tail = x[1]
        deg = head[0:-2]
        min = head[-2:]
        return deg + "deg" + min + "." + tail + "min"

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    gps = GPRMC_Parsing()

    rate = rospy.rate(10)

    while not rospy.is_shutdown():
        gps.parese_gprmc()
        rate.sleep()
