#!/usr/bin/env python3 
import rospy 
from std_msgs.msg import Int64 
from local_pkg.msg import Serial_Info 
 
class DR(): 
    def __init__(self): 
        rospy.Subscriber('/Displacement_right', Int64, self.encoderCallback) 
        rospy.Subscriber('/serial', Serial_Info, self.serialTopulse) 
 
        self.right = 0  # pulse from sensor 
        self.left = 0  # pulse from serial 
 
        self.gear = 0 
 
        self.dis = 0.0 
 
        self.init = 0 
        self.flag_filter = True 
        self.flag_dr = True 
 
        self.left_pulse = 0 
        self.right_pulse = 0 
        self.diff_left = 0 
        self.diff_right = 0 
 
        self.dis_left = 0 
        self.dis_right = 0 
        self.right_switch = False
        self.right_init = 0
 
        self.a = 0 
        self.b = 0 
        self.c = 0 
        self.d = 0 
 
    def encoderCallback(self, msg): 
        if self.right_switch == False :
            self.right_init = msg.data
            self.right_switch = True

        self.right = msg.data - self.right_init
 
    def filter(self): 
        if self.flag_filter: 
            self.left_pulse = self.left 
            self.right_pulse = self.right 
            self.flag_filter = False 
 
        if (abs(self.left - self.left_pulse) > 100): 
            self.left_pulse = self.left + self.diff_left 
        else: 
            self.diff_left = self.left - self.left_pulse 
            self.left_pulse = self.left 
 
        if (abs(self.right - self.right_pulse) > 100): 
            self.right_pulse = self.right + self.diff_right 
        else: 
            self.diff_right = self.right - self.right_pulse 
            self.right_pulse = self.right 
 
    def dead_reck(self): 
        if self.flag_dr: 
            self.a, self.b = self.left_pulse, self.left_pulse 
            self.c, self.d = self.right_pulse, self.right_pulse 
            self.flag_dr = False 
 
        elif self.flag_dr == False: 
            self.a = self.b 
            self.b = self.left_pulse 
 
            self.c = self.d 
            self.d = self.right_pulse 
 
        if ((self.b - self.a) < -10000000): 
            self.dis_left = (self.b + (256**4 - self.a)) / 60.852  # pulse to meter 
        else: 
            self.dis_left = (self.b - self.a)/60.852  # 1.6564/100 
 
        if ((self.d - self.c) < -10000000): 
            self.dis_right = (self.d + (256**4 - self.c)) / 60.852  # pulse to meter 
        else: 
            self.dis_right = (self.d - self.c)/60.852  # 1.6564/100 
 
        self.dis = (self.dis_left + self.dis_right) / 2 
 
    def serialTopulse(self, data): 
        self.gear = data.gear 
        if self.init == 0: 
            self.init = int(data.encoder[0]) + int(data.encoder[1])*256 \
                 + int(data.encoder[2])*256**2 + \
                    int(data.encoder[3])*256**3 
 
        self.left = int(data.encoder[0]) + int(data.encoder[1])*256 \
             + int(data.encoder[2])*256**2 + \
                int(data.encoder[3])*256**3 - self.init 
 
        self.filter() 
        self.dead_reck() 
 
if __name__ == '__main__': 
    try: 
        odometry = DR()
        rospy.spin()
    except rospy.ROSInterruptException: 
        pass