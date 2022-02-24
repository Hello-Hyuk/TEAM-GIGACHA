import rospy
# from lib.general_utils.ego_updater import egoUpdater
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.general_utils.read_global_path import read_global_path
from lib.controller_utils.pure_pursuit import PurePursuit
from lib.controller_utils.longtidudinal_controller import longitudinalController
from std_msgs.msg import String
from planner_and_control.msg import Path
from planner_and_control.msg import Control_Info
from planner_and_control.msg import Ego

class Controller:
    def __init__(self):
        rospy.init_node('controller', anonymous = False)
        rospy.Subscriber('/trajectory', Path, self.motion_callback)
        self.control_pub = rospy.Publisher('/controller', Control_Info, queue_size = 1)
        rospy.Subscriber('/ego', Ego, self.ego_callback)
        self.control_msg = Control_Info()

        self.ego = Ego()
        # self.trajectory = Path()          ## add motion trajectory 
        self.trajectory = read_global_path('all_nodes')
        self.target_speed = 5.0

        self.lat_controller = PurePursuit(self.ego, self.trajectory)
        self.lon_controller = longitudinalController(self.ego, self.target_speed)

    def motion_callback(self, msg):
        self.trajectory = msg
        
    def ego_callback(self, msg):
        self.ego = msg

    def run(self):
        self.publish_control_info(0,0)
        self.target_speed = 5.0

    def publish_control_info(self, estop, gear):
        self.control_msg.emergency_stop = estop
        self.control_msg.gear = gear
        self.control_msg.steer = self.lat_controller.run(self.ego)
        # ####################For PID Tuining
        # self.control_msg.steer = 0 
        #######################################
        # self.control_msg.speed, self.control_msg.brake = self.lon_controller.run()
        self.control_msg.speed, self.control_msg.brake = self.target_speed, 0
        self.control_pub.publish(self.control_msg)
        print("speed : ", self.control_msg.speed)
if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    cc = Controller()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        cc.run()
        rate.sleep()