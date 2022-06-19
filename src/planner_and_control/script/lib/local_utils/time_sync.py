#!/usr/bin/env python3
from std_msgs.msg import Time
import rospy

class Time_sync:
    def __init__(self):
        rospy.init_node("time",anonymous=True)
        self.pub = rospy.Publisher('/timer', Time, queue_size = 1)

        self.timer = Time()
        self.hz = rospy.get_param("Hz")

    def run(self):
        self.timer.data = rospy.Time.now()
        self.pub.publish(self.timer)

if __name__ == '__main__':
    ts = Time_sync()
    rate = rospy.Rate(ts.hz)

    while not rospy.is_shutdown():
        ts.run()
        rate.sleep()