#!/usr/bin/env python3 
from std_msgs.msg import Time 
import rospy 
 
rospy.init_node("time",anonymous=True) 
pub = rospy.Publisher('/timer', Time, queue_size = 1) 
 
test = Time() 
hz = rospy.get_param("Hz")
rate = rospy.Rate(hz) #hz 
 
while not rospy.is_shutdown(): 
    test.data = rospy.Time.now() 
    pub.publish(test) 
    rate.sleep()