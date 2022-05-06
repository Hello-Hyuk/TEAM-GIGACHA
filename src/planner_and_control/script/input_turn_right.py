import rospy
from lib.general_utils.sig_int_handler import Activate_Signal_Interrupt_Handler
from planner_and_control.msg import Perception

class Input_turn_right:
    def __init__(self):
        rospy.init_node('turn_right', anonymous = False)
        self.pub = rospy.Publisher("/input", Perception, queue_size = 1)
        self.perception = Perception()
        self.perception.tred = input("red(on : 1, off : 0) : ")
        self.perception.tyellow = input("yellow(on : 1, off : 0) : ")
        self.perception.tleft = input("left(on : 1, off : 0) : ")
        self.perception.tgreen = input("green(on : 1, off : 0) : ")
        
    def run(self):
        self.pub.publish(self.perception)
        print("input_turn_right is operating..")
        
if __name__ == "__main__":
    Activate_Signal_Interrupt_Handler()
    ss = Input_turn_right()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        ss.run()
        rate.sleep