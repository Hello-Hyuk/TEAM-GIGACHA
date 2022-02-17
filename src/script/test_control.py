#! /usr/bin/env python3

import rospy
import os
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32

rospy.init_node('testControl', anonymous=False)



def discallback(msg): #
    # 0 : distance
    # 1 : center_x   
    print("distance :", msg.data[0]) 
    print("center_x :", msg.data[1])
    
    # except:
    #     print('No Person Detected')
    
def listener():
    print("listener enter")
    rospy.Subscriber('/dis', Float32MultiArray, discallback) # class id , detecting only person


if __name__ == '__main__':
    print("==============")
    listener()
    print("-------------------")
    rospy.spin()
    



