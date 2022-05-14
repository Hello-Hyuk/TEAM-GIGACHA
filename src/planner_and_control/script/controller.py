#!/usr/bin/env python3

import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.controller_utils.pure_pursuit import PurePursuit
from lib.controller_utils.pi import PI
from std_msgs.msg import String
from planner_and_control.msg import Path, Control_Info, Ego

class LocalPath:
    def __init__(self):
        self.data = Path()

class ControlEgo:
    def __init__(self):
        self.data = Ego()

class Controller:
    def __init__(self):
        rospy.init_node('Controller', anonymous = False)
        rospy.Subscriber('/trajectory', Path, self.motion_callback)
        self.control_pub = rospy.Publisher('/controller', Control_Info, queue_size = 1)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        self.control_msg = Control_Info()

        self.ego = ControlEgo()
        self.trajectory = LocalPath()        ## add motion trajectory 
        self.target_speed = 5.0
        
        self.lat_controller = PurePursuit(self.ego, self.trajectory)
        self.lon_controller = PI(self.ego)

    def motion_callback(self, msg):
        self.trajectory.data = msg

    def ego_callback(self, msg):
        self.ego.data = msg
        
    def publish_control_info(self, estop, gear):
        self.control_msg.emergency_stop = estop
        self.control_msg.gear = gear
        try:
            self.control_msg.steer = self.lat_controller.run()
        except IndexError:
            print("++++++")
        # a = list(self.trajectory.data.x)
        # print(f"trajectory : {a[0]}")
        
        if self.ego.data.speed > self.ego.data.target_speed:
            self.control_msg.speed = self.lon_controller.decel()
        else:
            self.control_msg.speed = self.ego.data.target_speed

        self.control_msg.brake = 0       ## PID on
        # self.control_msg.speed, self.control_msg.brake = self.ego.data.target_speed, 0               ## PID off
        self.control_pub.publish(self.control_msg)

    def run(self):
        if len(self.trajectory.data.x) == 0:
            self.publish_control_info(1,0)
        else:
            self.publish_control_info(0,0)
        self.target_speed = 20.0
        # print("Controller On..")


if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    cc = Controller()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        cc.run()
        rate.sleep()
