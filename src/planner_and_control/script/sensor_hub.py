#!/usr/bin/env python3
import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Local, Obstacles
from sensor_msgs.msg import PointCloud
from planner_and_control.msg import Serial_Info
from planner_and_control.msg import Perception, Ego
from math import cos, sin, pi, sqrt
from geometry_msgs.msg import Polygon

class Sensor_hub:
    def __init__(self):
        rospy.init_node('Sensor_hub', anonymous = False)
        rospy.Subscriber("/pc1", PointCloud, self.Sensor_fusion_callback) # fusion
        rospy.Subscriber("/s1", Local, self.camera1_callback) # Camera 1
        rospy.Subscriber("/s3", Local, self.camera3_callback) # Camera 3
        rospy.Subscriber("/vision", Perception, self.vision_callback) # Camera
        rospy.Subscriber("/segments", Polygon, self.lidar_callback) # lidar
        rospy.Subscriber("/input", Perception, self.input_callback)
        rospy.Subscriber("/pose", Local, self.local_callback) # local_pose

        self.pub1 = rospy.Publisher("/perception", Perception, queue_size = 1)

        self.ego = Ego()
        self.perception = Perception()
        
    def local_callback(self, msg):
        self.ego.x = msg.x
        self.ego.y = msg.y
        self.ego.heading = msg.heading

    def camera1_callback(self, msg):
        pass

    def camera3_callback(self, msg):
        pass

    def Sensor_fusion_callback(self, msg):
        pass

    def vision_callback(self, msg):
        pass
    
    def lidar_callback(self, msg):        
        theta = (self.ego.heading) * pi / 180
        size = 0

        objx = []
        objy = []
        objr = []

        if len(msg.points) != 0:
            size = len(msg.points)//3
            for i in range(size):
        
                objx.append(msg.points[i+2].x * cos(theta) + msg.points[i+2].y * sin(theta) + self.ego.x)
                objy.append(msg.points[i+2].x * -sin(theta) + msg.points[i+2].y * cos(theta) + self.ego.y)
                objr.append(sqrt((msg.points[i+1].x - msg.points[i].x)**2 + (msg.points[i+1].y - msg.points[i].y)**2) / 2)

                self.perception.objx = objx
                self.perception.objy = objy
                self.perception.objr = objr

                print(objx)
                print(objy)
                print(objr)

        # # absolute coordinates transition
        # for i in range(len(msg.objx)):
        #     self.perception.obj.x.append(msg.objx[i] * cos(theta) + msg.objy[i] * -sin(theta) + self.ego.x)
        #     self.perception.obj.y.append(msg.objx[i] * sin(theta) + msg.objy[i] * cos(theta) + self.ego.y)
        # # radius calculation
        # msg.objr = abs((msg.objleft - msg.objright) / 2)

    def input_callback(self, msg):
        self.perception.signx = msg.signx
        self.perception.signy = msg.signy
        self.perception.objx = msg.objx
        self.perception.objy = msg.objy
        self.perception.objr = msg.objr
        self.perception.tred = msg.tred
        self.perception.tyellow = msg.tyellow
        self.perception.tleft = msg.tleft
        self.perception.tgreen = msg.tgreen
        self.perception.signname = msg.signname

    def run(self):
        self.pub1.publish(self.perception)
        # print("sensor_hub is operating..")

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    ss = Sensor_hub()
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        ss.run()
        rate.sleep()
