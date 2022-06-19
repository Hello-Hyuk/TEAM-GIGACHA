#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import Time
from planner_and_control.msg import Local
from lib.local_utils.gps import GPS
from lib.local_utils.imu import IMU

class Localization():
    def __init__(self):
        rospy.init_node('Localization', anonymous=False)

        self.pub = rospy.Publisher('/pose', Local, queue_size = 1)
        rospy.loginfo("============Localization On============")

        self.msg = Local()

        self.gps = GPS()
        self.imu = IMU()

    def main(self, msg):
        main_time = time.time()
        time_sync = None

        self.msg.x = self.gps.x
        self.msg.y = self.gps.y
        self.msg.orientation = self.imu.orientation_q

        if (main_time - self.gps.time) < 0.2 and (main_time - self.imu.time) < 0.2: # time syncronize
            time_sync = "Sync"
            if self.gps.heading_switch == True:
                offset = self.gps.heading - self.imu.heading
                self.msg.heading = self.imu.heading + offset # heading correction with gps heading
            else:
                self.msg.heading = self.imu.heading
        else:
            time_sync = "Unsync"
            self.msg.heading = self.imu.heading
        
        self.pub.publish(self.msg)

        rospy.loginfo("======================")
        rospy.loginfo("x : {0}, y : {1}".format(self.msg.x, self.msg.y))
        rospy.loginfo("heading : {0}, switch : {1}".format(self.msg.heading, self.gps.heading_switch))
        rospy.loginfo("time sync : {0}".format(time_sync))

if __name__ == '__main__':
    loc = Localization()
    rospy.Subscriber("/timer", Time, loc.main)