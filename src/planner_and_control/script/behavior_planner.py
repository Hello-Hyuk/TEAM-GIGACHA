#!/usr/bin/env python3
import rospy
from math import sqrt
from time import time
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from std_msgs.msg import String
from planner_and_control.msg import Ego
from planner_and_control.msg import Perception
from planner_and_control.msg import Sign

class Behavior_Planner:
    def __init__(self):
        rospy.init_node('Behavior_Planner', anonymous = False)
        rospy.Subscriber('/state', String, self.state_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/perception', Perception, self.perception_callback)
        self.pub_behavior = rospy.Publisher('/behavior', String, queue_size = 1)
        self.pub_ego = rospy.Publisher('/behavior_ego', Ego, queue_size = 1)
        self.ego = Ego()
        self.state = String()
        self.behavior = ""
        self.sign_dis = 100
        self.go_side_check = False
        self.wait_time = time()
        self.perception = Perception()

    def state_callback(self, msg):
        self.state = msg.data

    def ego_callback(self, msg):
        self.ego = msg

    def perception_callback(self, msg):
        self.perception = msg

    # def sign_callback(self, msg):
    #     self.sign_dis = sqrt((self.sign.x - self.ego.x)**2 + (self.sign.y - self.ego.y)**2)

    def run(self):
        
        if self.state == "go":
            self.behavior = "go"
            
        if self.state == "obstacle detected":
            self.behavior = "obstacle avoidance"

        sign_x = 63.7384548403
        sign_y = 111.167584983
        self.sign_dis = sqrt((sign_x - self.ego.x)**2 + (sign_y - self.ego.y)**2)

        if self.state == "stop_sign detected":
            if self.sign_dis <= 5:
                if self.go_side_check == False:
                    self.behavior = "stop"
                    self.wait_time = time()
                    self.go_side_check = True
                if self.behavior == "stop" and time() - self.wait_time > 3:
                    self.behavior = "go"
                    
            else:
                self.behavior = "go_side"
                self.go_side_check = False
                    
        print(f"behavior_planner : {self.behavior}")
        self.pub_behavior.publish(self.behavior)
        self.pub_ego.publish(self.ego)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    bp = Behavior_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        bp.run()
        rate.sleep