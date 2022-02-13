import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Hander
from lib.ego import Ego
from planner_and_control.msg import Local
from planner_and_control.msg import Serial_Info

class Sensor_hub:
    def __init__(self):
        rospy.init_node('Sensor_hub', anonymous = False)

        rospy.Subscriber("/pose", Local, self.localcallback) # local
        rospy.Subscriber("/sensor") # fusion
        rospy.Subscriber("/") # Camera 1
        rospy.Subscriber("/") # Camera 3
        rospy.Subscriber("/serial", Serial_Info, self.serial_callback)

    def localcallback(self, msg):

    def camera1_callback(self, msg):

    def camera3_callback(self, msg):

    def Sensor_fusion_callback(self, msg):

    def serial_callback(self, msg):

if __name__ == "__main__":
    Activate_Signal_Interrupt_Hander()
    ss = Sensor_hub()