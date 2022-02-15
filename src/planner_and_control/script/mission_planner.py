#!/usr/bin/env python3
import rospy
from lib.general_utils.ego import Ego
from lib.general_utils.sensor_hub import Sensor_hub
from lib.general_utils.read_global_path import read_global_path
from lib.planner_utils.index_finder import IndexFinder
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Hander
from std_msgs.msg import String

class Mission_Planner:
    def __init__(self):
        rospy.init_node('Mission_Planner', anonymous = False)
        self.pub = rospy.Publisher('/state', String, queue_size = 1)
        self.ego = Ego()
        self.ego.path = read_global_path('')
        self.state = ''
        self.sensor_hub = Sensor_hub()
        self.whereami = IndexFinder()

    def run(self):
        whereami.run()
        # if self.ego.status is "Ready"
        #     self.state "steady_state"
        # sample code
        a = 0
        b = 0
        if a == b:
            self.state = "go"
        #### sample code end
        print("mission_planner")
        self.pub.publish(self.state)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Hander()
    mm = Mission_Planner()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        mm.run()
        rate.sleep()
