import rospy
import serial
from std_msgs.msg import Int64
from planner_and_control.msg import Serial_Info
from planner_and_control.msg import Encoder

class Encdoer: # 1 rev per 100 pulse (when it goes straight)
    def __init__(self):
        rospy.init_node("Encoder", anonymous = False)
        rospy.Subscriber("/serial", Serial_Info, self.serialCallback)
        self.pub = rospy.Publisher('/encoder', Encoder, queue_size=1)
        self.ser = serial.Serial("/dev/encoder", 115200)
        self.encoder = Encoder()

        self.flag = True
        self.left_data = 0 # displacement [pulse]
        self.right_data = 0 # displacement [pulse]

        self.left = 0 
        self.right = 0

        self.diff_left = 0
        self.diff_right = 0

    def serialCallback(self, msg):
        self.left_data = msg.encoder

    def read_encoder(self):
        res = self.ser.readline()

        while True:
            try:
                print(int(res))
                break
            except:
                res = self.ser.readline()
        
        self.right_data = int(res)

    def filter(self):
        if self.flag:
            self.left = self.left_data
            self.right = self.right_data
            self.flag = False
        
        if (abs(self.left_data - self.left) > 100):
            self.left = self.left_data + self.diff_left
        else:
            self.diff_left = self.left_data - self.left
            self.left = self.left_data

        if (abs(self.right_data - self.right) > 100):
            self.right = self.right_data + self.diff_right
        else:
            self.diff_right = self.right_data - self.right # _data : past
            self.right = self.right_data # right : present

    def run(self):
        self.filter()

        self.encoder.left = self.left
        self.encoder.right = self.right

        self.pub.publish(self.encoder)


if __name__ == '__main__':
    enc = Encoder()
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        enc.run()
        rate.sleep()