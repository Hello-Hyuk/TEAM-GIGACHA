import rospy
from lib.general_utils.ego import Ego
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Hander
from std_msgs.msg import String

class Motion_Planner:
    def __init__(self):
        rospy.init_node('Motion_Planner', anonymous = False)
        rospy.Subscriber('/behavior', String, behavior_callback)
        self.pub = rospy.Publisher('/trajectory', String, queue_size = 1)
        self.ego = Ego()
        self.behavior = ""
        self.trajectory = " "
    
    def behavior_callback(self, msg):
        self.trajectory = msg

    def run(self):
        # sample code
        a = 0
        b = 0
        if a == b:
            self.trajectory = "go"
        #### sample code end

        pub.publish(self.trajectory)

if __name__ == "__main__":
    Activate_Signal_Interrupt_Hander()
    mp = Motion_Planner()
    if not rospy.is_shutdown():
        mp.run()