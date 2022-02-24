import rospy
from lib.general_utils.ego import Ego
from lib.general_utils.ego_updater import egoUpdater
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Hander
from std_msgs.msg import String
from planner_and_control.msg import Path
from planner_and_control.msg import Control_Info

class Controller:
    def __init__(self):
        rospy.init_node('controller', anonymous = False)
        rospy.Subscriber('/trajectory', Path, self.motion_callback)
        self.control_pub = rospy.Publisher('/controller', String, queue_size = 1)
        self.control_msg = String()

        self.ego = Ego()
        self.trajectory = String()          ## add motion trajectory 

        self.update_ego = egoUpdater(self.ego)
        self.ego.target_speed = 20.0

        self.lat_controller = PurePursuit(self.ego, self.trajectory)
        self.lon_controller = longitudinalController(self.ego)

    def motion_callback(self, msg):
        self.trajectory = msg
        
    def run(self):
        publish_control_info(0,0)
        self.ego.target_speed = 20.0

    def publish_control_info(self, estop, gear):
        self.control_msg.emergency_stop = estop
        self.control_msg.gear = gear
        self.control_msg.steer = self.lat_controller.run()
        # ####################For PID Tuining
        # self.control_msg.steer = 0 
        #######################################
        self.control_msg.speed, self.control_msg.brake = self.lon_controller.run()
        self.control_pub.publish(self.control_msg)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Hander()
    cc = Controller()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        cc.run()
        rate.sleep()