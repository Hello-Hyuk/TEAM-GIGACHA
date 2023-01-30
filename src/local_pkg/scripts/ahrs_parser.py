#!/usr/bin/env python3
import serial
import rospy
from sensor_msgs.msg import Imu
from sig_int_handler import Activate_Signal_Interrupt_Handler

class AHRS_Parsing: 
    def __init__(self):
        rospy.init_node("ahrs_raw", anonymous=False)
        rospy.loginfo('AHRS_Parsing : Serial connecting to /dev/imu')
        self.ser = serial.Serial(port = '/dev/imu', baudrate = 115200)

        self.raw_data = Imu()
        self.raw_data.header.stamp = rospy.Time.now()
        self.raw_data.header.frame_id = "imu_link"
        self.pub = rospy.Publisher("/imu", Imu, queue_size=1)
        self.data = ""

    def parser(self): 
        ser_read = self.ser.readline()
        try: # imu 센서의 raw data를 받아 ascii 코드 값으로 변환
            self.data = ser_read.decode('ascii')
        except:
            UnicodeDecodeError

        try: # imu 센서의 raw data를 사용하기 편리하게 각 변수에 parsing
            sdata = self.data.split(",")
            self.raw_data.orientation.x = float(sdata[3])
            self.raw_data.orientation.y = float(sdata[2])
            self.raw_data.orientation.z = float(sdata[1])
            self.raw_data.orientation.w = float(sdata[4]) # quaternion
            self.raw_data.angular_velocity.x = float(sdata[5])
            self.raw_data.angular_velocity.y = float(sdata[6])
            self.raw_data.angular_velocity.z = float(sdata[7]) # angular_velocity
            self.raw_data.linear_acceleration.x = float(sdata[8])
            self.raw_data.linear_acceleration.y = float(sdata[9])
            self.raw_data.linear_acceleration.z = float(sdata[11]) # state of charge
        except IndexError:
            rospy.loginfo("=============================")


        self.pub.publish(self.raw_data)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    imu = AHRS_Parsing() # imu센서의 raw data값을 parsing해서 ros통신 할 수있도록 publish
    try:
        while not rospy.is_shutdown():
            imu.parser()
    except rospy.ROSInitException:
        pass