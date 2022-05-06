#!/usr/bin/env python3
import rospy
from math import sqrt
from time import time
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.general_utils.mission import Mission
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
        self.mission = Mission(self.ego, self.perception)
        
        if self.state == "go":
            self.mission.go()
            
        if self.state == "parking":
            self.mission.parking()
            
        if self.state == "static obstacle detected":
            self.mission.static_obstacle(self.perception.objx, self.perception.objy)
            
        if self.state == "stop_sign detected":
            self.mission.stop()

        if self.state == "right_sign detected":
            self.mission.turn_right()

        print(f"behavior_planner : {self.ego.behavior_decision}")
        print(f"speed : {self.ego.target_speed}")
        
        self.behavior = self.ego.behavior_decision
        self.pub_behavior.publish(self.behavior)
        self.pub_ego.publish(self.ego)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    bp = Behavior_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        bp.run()
        rate.sleep