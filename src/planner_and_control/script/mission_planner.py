#!/usr/bin/env python3
import rospy
from math import sqrt
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String
from planner_and_control.msg import Perception
from planner_and_control.msg import Path
from planner_and_control.msg import Sign
from sensor_msgs.msg import PointCloud

class Mission_Planner:
    def __init__(self):
        rospy.init_node('Mission_Planner', anonymous = False)
        self.pub = rospy.Publisher('/state', String, queue_size = 1)
        rospy.Subscriber('/perception', Perception, self.perception_callback)
        rospy.Subscriber('/obj', Path, self.lidar_callback)
        # rospy.Subscriber('/sign', String, self.sign_callback)
        self.perception = Perception()
        self.state = ''
        self.obs_dis = 0
        self.sign = ''
        self.sign_dis = 100

    def perception_callback(self, msg):
        self.perception = msg

    def lidar_callback(self, msg):
        self.obstacle = msg
        self.obs_dis = sqrt(self.obstacle.x**2 + self.obstacle.y**2)

    # def sign_callback(self, msg):
    #     self.sign = msg
    #     self.sign_dis = sqrt((self.sign.x - self.perception.x)**2 + (self.sign.y - self.perception.y)**2)

    def run(self):

        if self.obs_dis < 15 :
            self.state = "obstacle detected"

        sign_x = 63.7384548403
        sign_y = 111.167584983

        self.sign_dis = sqrt((sign_x - self.perception.x)**2 + (sign_y - self.perception.y)**2)
        print(self.sign_dis)

        
        if self.sign_dis < 15:
            self.sign = "stop_sign"
            self.state = "stop_sign detected"
            
        else:
            self.state = "go"

        print(f"mission_planner : {self.state}")
        self.pub.publish(self.state)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    mm = Mission_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mm.run()
        rate.sleep()