#! /usr/bin/env python3

import rospy
import os
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32
from vision_msgs.msg import Detection2D
from vision_msgs.msg import Detection2DArray
from vision_msgs.msg import BoundingBox2D
from vision_msgs.msg import ObjectHypothesisWithPose
import math

rospy.init_node('test_subscriber', anonymous=False)


real_box_scale = 58353.5247088624
real_box_width = 325.03937008
focal_length = 132.2916666661539

def distance_finder(focal_length, real_box_width, box_width_in_frame):

    distance =  real_box_width * focal_length / box_width_in_frame
    return distance

global dis
def callback1(msg1): # bounding box
    try:
        msg=Float32()
        if len(msg1.detections) !=0:
            if index==0 and type(index) is int:
                msg = Float32MultiArray() # create Float32MultiArray type ros msg(std_msg)
                # print("Bbox width: ", msg1.detections[int(index)].bbox.size_x)
                bbox_width = msg1.detections[int(index)].bbox.size_x
                # print("Bbox height: ", msg1.detections[int(index)].bbox.size_y)
                # scale = msg1.detections[int(index)].bbox.size_x * msg1.detections[int(index)].bbox.size_y
                # print("Bbox : ", scale)
                dis = distance_finder(focal_length,real_box_width, bbox_width)
                cx = msg1.detections[int(index)].bbox.center.x
                msg.data = []
                msg.data = [dis/(10**3), cx * 0.0002645833]
                print("Distance :", dis)
                pub.publish(msg)
    
    except IndexError:
        print("No RedHand Dector")

    # except:
    #     print('No Person Detected')
    
def callback2(msg2): # confidence
    try:
        if len(msg2.data)!=0:
            if index==0 and type(index) is int: print(" ")
    except IndexError:
        print("No RedHand Dector")


def callback3(msg3): # class id
    #global PPP # for only person
    # PPP = 'fuck' # for only person
    global index
    index='None'
    if len(msg3.data)!=0:
        if 0 in msg3.data:
            index=msg3.data.index(0)
            #print("clss: ",msg3.data[index])
        else:
            print("No RedHand Dector")
        # for i in range(len(msg3.data)):
        #     if msg3.data[i]==0: # person class is number 0
        #         PPP = i
        #         print("clss: ", msg3.data[i])
    #os.system('cls' if os.name =='nt' else 'clear')
    


def listener():
    rospy.Subscriber('/clss', Float32MultiArray, callback3) # class id , detecting only person
    rospy.Subscriber('/confs', Float32MultiArray, callback2) # confidence
    rospy.Subscriber('/bbox', Detection2DArray, callback1) # bouding box width, height
    

#def talker():
    



if __name__ == '__main__':
    listener()
    pub = rospy.Publisher('/dis', Float32MultiArray , queue_size=10) # create dis msg
    
    #talker()
    rospy.spin()
    