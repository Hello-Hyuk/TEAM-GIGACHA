#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose, PoseStamped
from planner_and_control.msg import Local
from ublox_msgs.msg import NavPVT

from lib.local_utils.gps import GPS
from lib.local_utils.imu import IMU

class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous=False)
        self.pub = rospy.Publisher('/pose', Local, queue_size = 1)
        self.msg = Local()

        self.vis_pub = rospy.Publisher('/vis_pose', PoseStamped, queue_size=1)
        self.vis_msg = PoseStamped()
        self.vis_msg.header.frame_id = "map"

        self.gps = GPS()
        self.imu = IMU()

    def main(self):
        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.heading = self.imu.yaw

        self.vis_msg.pose.position.x = self.msg.x
        self.vis_msg.pose.position.y = self.msg.y
        self.vis_msg.pose.position.z = self.msg.heading

        self.pub.publish(self.msg)
        self.vis_pub.publish(self.vis_msg)

        print(self.msg)

if __name__ == '__main__':
    loc = Localization()
    rate = rospy.Rate(100)
 
    while not rospy.is_shutdown():
        loc.main()
        rate.sleep()