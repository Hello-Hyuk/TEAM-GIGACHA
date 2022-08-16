import rospy
import math
from std_msgs.msg import Time
from planner_and_control.msg import Displacement
from lib.local_utils.imu import IMU
from lib.local_utils.gps import GPS


class DR:
    def __init__(self):
        rospy.Subscriber("/encoder", Displacement, self.encoderCallback)
        rospy.Subscriber("/timer", Time, self.dead_reckoning)

        self.imu = IMU()
        self.gps = GPS()

        self.x = self.gps.x # initial position
        self.y = self.gps.y # initial position
        self.velocity = 0        

        self.left = 0 #[pulse]
        self.right = 0 #[pulse]

        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0

        self.flag = True

    def encoderCallback(self, msg):
        self.left = msg.left # saved pulse
        self.right = msg.right

    def dead_reckoning(self, msg):
        if self.flag:
            self.a = self.left
            self.b = self.left
            self.c = self.right
            self.d = self.right
            self.flag = False

        elif self.flag == False:
            self.a = self.b
            self.b = self.left

            self.c = self.d
            self.d = self.right

        if ((self.b - self.a) < -10000000):
            dis_left = (self.b + (256**4 - self.a))/60.852 # pulse to meter
        else:
            dis_left = (self.b - self.a)/60.852 # 1.6564/100

        if ((self.d - self.c) < -10000000):
            dis_right = (self.d + (256**4 - self.a))/60.852
        else:
            dis_right = (self.d - self.c)/60.852

        dis = (dis_right + dis_left) / 2

        self.velocity = dis/0.1

        self.x += dis*math.cos(math.radians(self.imu.heading))
        self.y += dis*math.sin(math.radians(self.imu.heading))

if __name__ == '__main__':
    try:
        dr=DR()
    except rospy.ROSInterruptException:
        pass