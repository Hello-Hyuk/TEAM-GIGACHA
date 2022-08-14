#!/usr/bin/env python3
import threading
from time import sleep
from .sub_function.mission import Mission
from std_msgs.msg import String


class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared

        self.ego = self.shared.ego
        self.perception = self.shared.perception
        self.plan = self.shared.plan

        self.behavior = " "
        self.sign_dis = 100
        self.traffic_dis = 100
        self.go_side_check = False
        self.sign_detected = 0  # action just one time
        self.mission = Mission(self.shared, self.ego,
                               self.perception, self.plan)
        self.state_remember = "go"

    def run(self):
        while True:
            try:
                self.mission.convert_lidar()

                if self.state_remember != self.plan.state:
                    self.state_remember = self.plan.state
                    self.mission.time_checker = False

                if self.plan.state == "parking":
                    self.mission.Parking()

                elif self.plan.state == "static_obstacle_detected":
                    self.mission.static_obstacle()

                elif self.plan.state == "stop_sign_detected":
                    self.mission.stop()

                elif self.plan.state == "right_sign_detected":
                    self.mission.turn_right()

                elif self.plan.state == "left_sign_detected":
                    self.mission.turn_left()

                elif self.plan.state == "child_area":
                    self.mission.child_area(
                        self.shared.perception.signx, self.shared.perception.signy)

                elif self.plan.state == "right_sign_area":
                    self.mission.non_traffic_right()

                elif self.plan.state == "emergency_stop":
                    self.mission.emergency_stop()

                elif self.plan.state == "delivery":
                    self.mission.pickup()

                else:
                    self.mission.go()

            except IndexError:
                # pass
                print("++++++++behavior_controller+++++++++")

            sleep(self.period)
