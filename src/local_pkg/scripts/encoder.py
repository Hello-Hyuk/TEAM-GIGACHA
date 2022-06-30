import rospy
import serial
from std_msgs.msg import Int64
from planner_and_control.msg import Serial_Info
from planner_and_control.msg import Displacement

class DP: # 1 rev per 100 pulse (when it goes straight)
    def __init__(self):
        rospy.init_node('Encoder', anonymous = False)
        rospy.Subscriber("/serial", Serial_Info, self.serialCallback)
        self.pub = rospy.Publisher('/encoder', Displacement, queue_size=1)
        self.ser = serial.Serial(port = '/dev/encoder', baudrate = 115200)
        self.encoder = Displacement()

        self.flag = True
        self.left_data = 0 # displacement [pulse]
        self.right_data = 0 # displacement [pulse]

        self.left = 0 
        self.right = 0

        self.diff_left = 0
        self.diff_right = 0

        self.init = 0

    def serialCallback(self, msg):
        self.read_encoder()
        data = msg.encoder
        if self.init == 0:
            self.init = int(data[0]) + int(data[1])*256\
                 + int(data[2])*256**2 + int(data[3])*256**3

        self.left_data = int(data[0]) + int(data[1])*256\
                 + int(data[2])*256**2 + int(data[3])*256**3 - self.init

    def read_encoder(self):
        res = self.ser.readline()
        try:
            data = res.decode('ascii')
            self.right_data = int(data)
        except:
            UnicodeDecodeError
        
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
    enc = DP()
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        enc.run()
        rate.sleep()