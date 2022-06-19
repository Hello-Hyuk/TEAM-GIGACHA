import rospy
import math
from std_msgs.msg import Time
from planner_and_control.msg import Encoder
from lib.local_utils.imu import IMU


class DR:
    def __init__(self):
        rospy.init_node("DeadReckoning", anonymous=False)
        rospy.Subscriber("/encoder", Encoder, self.encoderCallback)
        rospy.Subscriber("/timer", Time, self.dead_reckoning)

        self.x = 0.0
        self.y = 0.0
        self.velocity = 0.0
        self.imu = IMU()

        self.left = 0 #[pulse]
        self.right = 0 #[pulse]

        self.flag = True

    def encoderCallback(self, msg):
        self.left = msg.left # saved pulse
        self.right = msg.right

    def dead_reckoning(self, msg):
        if self.flag and self.left !=0:
            a = self.left
            b = self.left
            c = self.right
            d = self.right
            self.flag = False

        elif self.flag == False:
            a = b
            b = self.left

            c = d
            d = self.right

        if ((b - a) < -10000000):
            dis_left = (b + (256**4 - a))/60.852 # pulse to meter
        else:
            dis_left = (b - a)/60.852 # 1.6564/100

        if ((d - c) < -10000000):
            dis_right = (d + (256**4 - a))/60.852
        else:
            dis_right = (d - c)/60.852

        dis = (dis_right + dis_left) / 2

        self.velocity = dis/0.1

        self.x += dis*math.cos(math.radians(self.imu.heading))
        self.y += dis*math.sin(math.radians(self.imu.heading))

if __name__ == '__main__':
    try:
        dr=DR()
    except rospy.ROSInterruptException:
        pass