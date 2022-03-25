#!/usr/bin/env python3
import rospy
from math import sqrt
import time
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String
from planner_and_control.msg import Ego
from planner_and_control.msg import Sign

class Behavior_Planner:
    def __init__(self):
        rospy.init_node('Behavior_Planner', anonymous = False)
        rospy.Subscriber('/state', String, self.state_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        # rospy.Subscriber('/sign', Sign, self.sign_callback)
        self.pub = rospy.Publisher('/behavior', String, queue_size = 1)
        self.ego = Ego()
        self.state = String()
        self.behavior = ""
        self.sign_dis = 100

    def state_callback(self, msg):
        self.state = msg.data

    def ego_callback(self, msg):
        self.ego = msg

    # def sign_callback(self, msg):
    #     self.sign_dis = sqrt((self.sign.x - self.ego.x)**2 + (self.sign.y - self.ego.y)**2)

    def run(self):
        
        if self.state == "go":
            self.behavior = "go"
            
        if self.state == "obstacle detected":
            self.behavior = "obstacle avoidance"

        sign_x = 37.239875
        sign_y = 126.77362833333
        self.sign_dis = sqrt((sign_x - self.ego.x)**2 + (sign_y - self.ego.y)**2)

        if self.state == "stop_sign detected":
            self.behavior = "go_side"
            if self.sign_dis <= 1:
                if self.behavior == "go_side":
                    self.behavior = "stop"
                    time.sleep(3)
                if self.behavior == "stop":
                    self.behavior = "return"
                
                    
        print(f"behavior_planner : {self.behavior}")
        self.pub.publish(self.behavior)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    bp = Behavior_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        bp.run()
        rate.sleep