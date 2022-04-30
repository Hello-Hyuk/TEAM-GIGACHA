#!/usr/bin/env python3
import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.planner_utils.index_finder import IndexFinder
from planner_and_control.msg import Local
from sensor_msgs.msg import PointCloud
from planner_and_control.msg import Serial_Info
from planner_and_control.msg import Perception
from planner_and_control.msg import Obj


class Sensor_hub:
    def __init__(self):
        rospy.init_node('Sensor_hub', anonymous = False)
        rospy.Subscriber("/pc1", PointCloud, self.Sensor_fusion_callback) # fusion
        rospy.Subscriber("/s1", Local, self.camera1_callback) # Camera 1
        rospy.Subscriber("/s3", Local, self.camera3_callback) # Camera 3

        self.pub1 = rospy.Publisher("/perception", Perception, queue_size = 1)
        self.pub2 = rospy.Publisher("/obj", Obj, queue_size = 1) # perception
        self.obj = Obj()
        self.perception = Perception()
        self.perception.signx = [63.7384548403, 0]
        self.perception.signy = [111.167584983, 0]

    def camera1_callback(self, msg):
        pass

    def camera3_callback(self, msg):
        pass

    def Sensor_fusion_callback(self, msg):
        pass

    def run(self):
        self.pub1.publish(self.perception)
        self.pub2.publish(self.obj)

        print("sensor_hub is operating..")

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    ss = Sensor_hub()
    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        ss.run()
        rate.sleep
        
