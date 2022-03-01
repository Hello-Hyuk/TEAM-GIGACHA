import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from lib.planner_utils.index_finder import IndexFinder
from lib.general_utils.read_global_path import read_global_path
from planner_and_control.msg import Local
from planner_and_control.msg import Serial_Info
from planner_and_control.msg import Ego

class Sensor_hub:
    def __init__(self):
        rospy.init_node('Sensor_hub', anonymous = False)
        rospy.Subscriber("/pose", Local, self.localcallback) # local
        rospy.Subscriber("/sensor", Local, self.Sensor_fusion_callback) # fusion
        rospy.Subscriber("/s1", Local, self.camera1_callback) # Camera 1
        rospy.Subscriber("/s3", Local, self.camera3_callback) # Camera 3
        rospy.Subscriber("/serial", Serial_Info, self.serial_callback) # serial

        self.pub = rospy.Publisher("/ego", Ego, queue_size = 1)
        self.ego = Ego()
        self.IF = IndexFinder(self.ego)

    def localcallback(self, msg):
        print("do")
        self.ego.x = msg.x
        self.ego.y = msg.y
        self.ego.heading = msg.heading
        self.index = self.IF.run()

        self.ego.index = self.index

    def camera1_callback(self, msg):
        pass

    def camera3_callback(self, msg):
        pass

    def Sensor_fusion_callback(self, msg):
        pass

    def serial_callback(self, msg):
        self.ego.speed = msg.speed
        self.ego.steer = msg.steer
        self.ego.brake = msg.brake
        self.ego.gear = msg.gear
        self.ego.auto_manual = msg.auto_manual

    def run(self):
        self.pub.publish(self.ego)
        print("sensor_hub is operating..")

if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    ss = Sensor_hub()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        ss.run()
        rate.sleep
        
