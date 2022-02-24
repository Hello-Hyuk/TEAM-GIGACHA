from planner_and_control.msg import Serial_Info
from std_msgs.msg import String
import rospy

class egoUpdater:
    def __init__(self, ego):
        self.ego = ego

        rospy.Subscriber("/state", String, self.plannerCallback)
        rospy.Subscriber("/serial", Serial_Info, self.serialCallback)


    def plannerCallback(self, msg):
        self.ego.index = msg.index
        self.ego.x = msg.local.x
        self.ego.y = msg.local.y
        self.ego.heading = msg.local.heading
        # self.ego.mode = msg.mode
        
    def serialCallback(self, msg):
        self.ego.auto_manual = msg.auto_manual
        self.ego.steer = msg.steer
        self.ego.speed = msg.speed
        self.ego.brake = msg.brake
        self.ego.gear = msg.gear
        
        