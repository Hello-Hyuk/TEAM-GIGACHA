#!/usr/bin/env python3
import serial
import rospy

class GNGGA_Parsing:
    def __init__(self):
        self.ser = serial.Serial('/dev/gps', baudrate = 115200)
        print('GNGGA_Parsing : Serial connecting to /dev/gps')

        self.lat = 0.0
        self.lon = 0.0
        self.status = ""
        self.satellite = ""
        self.noise = ""

        self.data = ""


    def parese_gngga(self):
        ser_read = self.ser.readline()
        try:
            self.data = ser_read.decode('ascii')
        except:
            UnicodeDecodeError

        # print(self.data)

        if self.data[0:6] == "$GNGGA":
            # print("ok")
            sdata = self.data.split(",")
            
            if sdata[6] == "0":
                print("GNGGA_Parsing : No satellite data available")
                return

            print("=========Parsing GNGGA=========")
            self.lat = self.make_decode(sdata[2])
            self.lon = self.make_decode(sdata[4])
            self.status = sdata[6]
            self.satellite = sdata[7]
            self.noise = sdata[8]

    def make_decode(self, coord):
        x = coord.split(".")
        head = x[0]
        tail = x[1]
        deg = head[0:-2]
        min = head[-2:]
        return float(deg + "." + min + tail)

if __name__ == "__main__":
    gps = GNGGA_Parsing()

    while not rospy.is_shutdown():
        gps.parese_gngga()
