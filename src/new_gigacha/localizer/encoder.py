import threading
import rospy
from time import sleep
from local_pkg.msgs.msg import Displacement
 
class Encoder(threading.Thread): # 1 rev per 100 pulse (when it goes straight) 
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.odometry = parent.shared.dp #[pulse]
        self.ego = parent.shared.ego

        rospy.Subscriber('/encoder', Displacement, self.encoderCallback)

        self.flag = True 
        self.left_data = 0 # displacement [pulse] 
        self.right_data = 0 # displacement [pulse] 
 
        self.diff_left = 0 
        self.diff_right = 0 
 
        self.init = 0

    def encoderCallback(self, msg):
        self.right_data = msg.data

        if self.init == 0:
            self.init = int(self.ego.encoder[0]) + int(self.ego.encoder[1])*256\
                + int(self.ego.encoder[2])*256**2 + int(self.ego.encoder[3])*256**3

        self.left_data = int(self.ego.encoder[0]) + int(self.ego.encoder[1])*256\
                + int(self.ego.encoder[2])*256**2 + int(self.ego.encoder[3])*256**3 - self.init
 
    def filter(self): 
        if self.flag: 
            self.odometry.left = self.left_data 
            self.odometry.right = self.right_data 
            self.flag = False 
          
        if (abs(self.left_data - self.odometry.left) > 100): 
            self.odometry.left = self.left_data + self.diff_left 
        else: 
            self.diff_left = self.left_data - self.odometry.left 
            self.odometry.left = self.left_data 
 
        if (abs(self.right_data - self.odometry.right) > 100): 
            self.odometry.right = self.right_data + self.diff_right 
        else: 
            self.diff_right = self.right_data - self.odometry.right # _data : past 
            self.odometry.right = self.right_data # right : present 
 
    def run(self):
        while True:
            self.filter()

            sleep(self.period)