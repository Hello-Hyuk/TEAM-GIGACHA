import threading
import numpy as np
import rospy
from local_pkg.msg import Control_Info
from time import sleep
from math import hypot, cos, sin, degrees, atan2, radians, pi,sqrt, tan

class LonController(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego
        self.plan = parent.shared.plan

        self.car_max_speed = 10
        self.road_friction = 0.15

        self.serial_pub = rospy.Publisher("controller", Control_Info, queue_size=1)

    def curve_based_velocity(self):
        self.ego.input_speed = (1.04 / tan(self.ego.steer)) - 2 # 2 will be tuned

    def run(self): 
        while True:
            try:
                # path = self.lattice_path[self.shared.selected_lane]
                # self.speed = self.curve_based_velocity(path,20)
                
                # self.speed = self.velocity_based_curve(path, 30)
                # self.ego.input_speed = self.speed[0]
                self.curve_based_velocity()
                
                self.ego.input_estop = self.ego.target_estop
                self.ego.input_speed = self.ego.target_speed
                self.ego.input_gear = self.ego.target_gear
                self.ego.input_brake = self.ego.target_brake
                if self.ego.target_estop == 0:
                    self.ego.input_estop = 0x00
                elif self.ego.target_estop == 1:
                    self.ego.input_estop = 0x01

                ######################## SERIAL ################################
                serial = Control_Info()
                serial.emergency_stop = self.ego.input_estop
                serial.gear = self.ego.input_gear
                serial.speed = self.ego.input_speed
                serial.steer = self.ego.input_steer
                serial.brake = self.ego.input_brake

                self.serial_pub.publish(serial)

            except IndexError:
                print("++++++++lon_controller+++++++++")

            sleep(self.period)