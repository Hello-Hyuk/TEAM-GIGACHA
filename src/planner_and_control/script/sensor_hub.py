import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Hander
from lib.general_utils.ego import Ego
from planner_and_control.msg import Local
from planner_and_control.msg import Serial_Info

class Sensor_hub:
    def __init__(self):
        rospy.init_node('Sensor_hub', anonymous = False)

        rospy.Subscriber("/pose", Local, self.localcallback) # local
        rospy.Subscriber("/sensor", Local, self.localcallback) # fusion
        rospy.Subscriber("/s", Local, self.localcallback) # Camera 1
        rospy.Subscriber("/s", Local, self.localcallback) # Camera 3
        rospy.Subscriber("/serial", Serial_Info, self.serial_callback) # serial

    def localcallback(self, msg):
        pass

    def camera1_callback(self, msg):
        pass

    def camera3_callback(self, msg):
        pass

    def Sensor_fusion_callback(self, msg):
        pass

    def serial_callback(self, msg):
        pass

if __name__ == "__main__":
    Activate_Signal_Interrupt_Hander()
    ss = Sensor_hub()