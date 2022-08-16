#!/usr/bin/env python3
from re import A
import threading
from time import sleep
from sub_function.motion import Motion
from sub_function.find_local_path import findLocalPath
#from .sub_function.LPP import path_maker  # LPP 구현 하기

class MotionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.plan = parent.shared.plan
        self.ego = parent.shared.ego

        # self.trajectory = self.plan.trajectory # to controller
        self.global_path = self.shared.global_path # from localizer
        self.cut_path = self.shared.cut_path # from global path (find_local_path)
        self.lattice_path = self.shared.lattice_path # from LPP []

        self.lane_weight = [10000, 0, 10000]
        self.isObstacle = [1000, 1000, 1000]
        
        self.motion = Motion(self.shared, self.plan, self.ego)

    
    def run(self):
        while True:
            # print(len(self.global_path.x))
            findLocalPath(self.global_path, self.ego, self.cut_path) # from global path (50indexes)
            self.motion.path_maker() # lattice_path

            # print(len(self.lattice_path))

            if self.shared.plan.behavior_decision == "static_obstacle_avoidance":
                self.motion.weight_function_obstacle_avoidance()
                self.motion.select_trajectory()
            
            elif self.shared.plan.behavior_decision == "go_side":
                # self.weight_sign_function()
                self.motion.select_trajectory()
            
            # elif self.shared.plan.behavior_decision == "stop":
            #     self.plan.trajectory.x = []
            #     self.plan.trajectory.y = []

            elif self.shared.plan.behavior_decision == "turn_right":
                self.lane_weight = [10000, 10000, 0]
                self.motion.select_trajectory()

            elif self.shared.plan.behavior_decision == "turn_left":
                self.lane_weight = [10000, 0, 10000]
                self.motion.select_trajectory()

            elif self.shared.plan.behavior_decision == "driving":
                # print(self.shared.plan.behavior_decision)
                self.motion.select_trajectory()

            # print(self.trajectory.x)
            sleep(self.period)