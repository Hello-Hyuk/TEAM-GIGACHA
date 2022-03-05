import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.general_utils.read_global_path import read_global_path
from lib.controller_utils.pure_pursuit import PurePursuit
from lib.controller_utils.longtidudinal_controller import longitudinalController
from std_msgs.msg import String
from planner_and_control.msg import Path
from planner_and_control.msg import Control_Info
from planner_and_control.msg import Ego

class LocalPath:
    def __init__(self):
        self.data = Path()

class ControlEgo:
    def __init__(self):
        self.data = Ego()

class Controller:
    def __init__(self):
        rospy.init_node('controller', anonymous = False)
        rospy.Subscriber('/local_path', Path, self.motion_callback)
        self.control_pub = rospy.Publisher('/controller', Control_Info, queue_size = 1)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        self.control_msg = Control_Info()

        self.ego = ControlEgo()
        self.trajectory = LocalPath()        ## add motion trajectory 
        self.target_speed = 20.0
        
        self.lat_controller = PurePursuit(self.ego, self.trajectory)
        self.lon_controller = longitudinalController(self.ego, self.target_speed)

    def motion_callback(self, msg):
        self.trajectory.data = msg

    def ego_callback(self, msg):
        self.ego.data = msg
        
    def run(self):
        self.publish_control_info(0,0)
        self.target_speed = 20.0
        # print("Controller On..")

    def publish_control_info(self, estop, gear):
        self.control_msg.emergency_stop = estop
        self.control_msg.gear = gear
        try:
            self.control_msg.steer = self.lat_controller.run()
        except IndexError:
            print("++++++")

        #self.control_msg.speed, self.control_msg.brake = self.lon_controller.run()         ## PID off
        self.control_msg.speed, self.control_msg.brake = self.target_speed, 0               ## PID on
        self.control_pub.publish(self.control_msg)


if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    cc = Controller()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        cc.run()
        rate.sleep()
