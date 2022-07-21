#!/usr/bin/env python3
import rospy
import serial
from local_pkg.msg import Displacement

class Encoder_Parsing: # 1 rev per 100 pulse (when it goes straight)
    def __init__(self):
        rospy.init_node('Encoder', anonymous = False)
        self.pub = rospy.Publisher('/encoder', Displacement, queue_size=1)
        self.ser = serial.Serial(port = '/dev/ttyACM0', baudrate = 115200)
        self.encoder = Displacement()

        self.right_data = 0

    def read_encoder(self):
        res = self.ser.readline()
        try:
            data = res.decode('ascii')
            self.right_data = int(data)
            self.pub.publish(self.right_data)
        except UnicodeDecodeError:
            pass
            

if __name__ == '__main__':
    enc = Encoder_Parsing()
    rate = rospy.Rate(20)

    while not rospy.is_shutdown():
        enc.read_encoder()
        rate.sleep()