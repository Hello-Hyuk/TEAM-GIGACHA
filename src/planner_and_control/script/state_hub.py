#!/usr/bin/env python3

from ast import Str
import rospy
from std_msgs.msg import String
from planner_and_control.msg import Path, Control_Info, Ego, Perception

class State_hub:
    def __init__(self):
        rospy.init_node('State_Hub', anonymous = False)

        rospy.Subscriber('/state', String, self.state_callback) #mission
        rospy.Subscriber('/behavior', String, self.behavior_callback)
        rospy.Subscriber('/ego', Ego, self.ego_callback) #behavior
        rospy.Subscriber('/trajectory', Path, self.motion_callback) 
        rospy.Subscriber('/controller',Control_Info, self.control_callback)
        rospy.Subscriber('/perception',Perception, self.perception_callback)
        self.state = ""
        self.behavior = ""
        self.motion = Path()
        self.control_msg = Control_Info()
        self.ego = Ego()
        self.control = Control_Info()
        self.perception = Perception()

    def ego_callback(self, msg):
        self.ego = msg

    def state_callback(self, msg):  #mission_planner callback
        self.state = msg.data

    def behavior_callback(self, msg):  #behavior_planner
        self.behavior = msg.data

    def motion_callback(self, msg):
        self.motion = msg

    def control_callback(self, msg):
        self.control = msg

    def perception_callback(self, msg):
        self.perception = msg

    def run(self):
        print(f"------------------------------------------------------\n[map_name] \n {self.ego.map_file}\n\n[mission_planner]\n{self.state}\n\nbehavior_planner]\n{self.behavior}\n\n[motion_planner]\nselect line : {self.motion.select_lane}\n\n[control_info]\n{self.control}\n\n[sing_name]\n{self.perception.signname}\n------------------------------------------------------\n")
        



if __name__ == "__main__":
    A = State_hub()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        A.run()
        rate.sleep