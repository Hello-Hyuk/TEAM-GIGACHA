import rospy
from lib.ego

class Sensor_hub:
    def __init__(self):
        rospy.init_node('Sensor_hub', anonymous = False)

        rospy.Subscriber("/pose") # local
        rospy.Subscriber("/sensor") # fusion
        rospy.Subscriber("/") # Camera 1
        rospy.Subscriber("/") # Camera 3

    def localcallback(self, msg):

    def camera1_callback(self, msg):

    def camera3_callback(self, msg):

    def Sensor_fusion_callback(self, msg):