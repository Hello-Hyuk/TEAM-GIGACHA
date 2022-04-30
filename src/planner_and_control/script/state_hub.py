import rospy
from std_msgs.msg import String
from planner_and_control.msg import Obj, Path, Control_Info
#, Behavior_Info

class State_hub:
    def __init__(self):
        rospy.init_node('state_hub', anonymous=False)
        rospy.Subscriber('/obj', Obj, self.obj_callback) #sensor_hub
        rospy.Subscriber('/state', String, self.state_callback) #mission
        rospy.Subscriber('/behavior', String, self.behavior_callback) #behavior
        rospy.Subscriber('/trajectory', Path, self.motion_callback) 
        rospy.Subscriber('/controller',Control_Info, self.control_callback)
        self.control_msg = Control_Info()
        #self.behavior = Behavior_Info()
        self.obj = Obj()
        self.motion = Path()
        self.sign = ""
        self.behavior = ""
        self.state = ""

    def obj_callback(self, msg):  #sensor_hub callback
        self.sign = msg

    def state_callback(self, msg):  #mission_planner callback
        self.state = msg

    def behavior_callback(self, msg): 
        self.behavior = msg

    def motion_callback(self, msg):
        self.motion = msg

    def control_callback(self, msg):
        self.control_msg = msg

    

    def run(self):
        print("---sensor_hub--- ")
        print(self.sign)
        print("---mission_planner---")
        print (self.state)
        print("---behavior_planner---")
        print(self.behavior)
        print("---motion_planner--- : ")
        #print(self.motion)
        print("---controll_info---")
        print(self.control_msg.speed)


if __name__ == "__main__":
    A = State_hub()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        A.run()
        rate.sleep
        