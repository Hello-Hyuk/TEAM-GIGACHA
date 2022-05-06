import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Local
from sensor_msgs.msg import PointCloud

class Input_turn_right:
    def __init__(self):
        rospy.init_node('trun_right', anonymous = False)
        rospy.Subscriber("/")