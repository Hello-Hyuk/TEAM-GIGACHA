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

        rospy.Subscriber('/ego', Ego, self.ego_callback)
        rospy.Subscriber('/perception', Perception, self.perception_callback)
        rospy.Subscriber('/state', String, self.state_callback)

        self.pub_behavior = rospy.Publisher('/behavior', String, queue_size = 1)
        self.pub_ego = rospy.Publisher('/behavior_ego', Ego, queue_size = 1)

        self.ego = Ego()
        self.perception = Perception()
        self.state = String()

        self.behavior = ""
        self.sign_dis = 100
        self.traffic_dis = 100
        self.go_side_check = False
        self.sign_detected = 0 # action just one time
        self.wait_time = time()
        

    def ego_callback(self, msg):
        self.ego = msg

    def perception_callback(self, msg):
        self.perception = msg

    def state_callback(self, msg):
        self.state = msg.data

    def run(self):
        
        if self.state == "go":
            self.behavior = "go"
            
        if self.state == "obstacle detected":
            self.behavior = "obstacle avoidance"

        if self.state == "stop_sign detected":
            self.sign_dis = sqrt((self.perception.signx[0] - self.ego.x)**2 + (self.perception.signy[0] - self.ego.y)**2)
            if self.sign_dis <= 5:
                if self.go_side_check == False:
                    self.behavior = "stop"
                    self.wait_time = time()
                    self.go_side_check = True
                if self.behavior == "stop" and time() - self.wait_time > 3:
                    self.behavior = "go"
                    self.sign_detected = 1
            elif self.sign_dis > 5 and self.sign_detected == 0:
                self.behavior = "go_side"
                self.go_side_check = False

        if self.state == "right_sign detected":
            if self.perception.tgreen == 1:
                self.behavior = "turn_right"
            else:
                if self.perception.stop == 1:
                    self.behavior = "stop"
                else:
                    self.behavior = "turn_right"
                
                    
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