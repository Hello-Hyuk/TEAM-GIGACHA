#!/usr/bin/env python3
from re import A
import threading
from time import sleep
from .sub_function.motion import Motion
from .sub_function.find_local_path import findLocalPath
#from .sub_function.LPP import path_maker  # LPP 구현 하기

class MotionPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.plan = parent.shared.plan
        self.ego = parent.shared.ego

        self.global_path = self.shared.global_path # from localizer
        self.cut_path = self.shared.cut_path # from global path (find_local_path)
        self.lattice_path = self.shared.lattice_path # from LPP []
        
        self.motion = Motion(self.shared, self.plan, self.ego)
    
    def run(self):
        while True:
            findLocalPath(self.global_path, self.ego, self.cut_path) # from global path (50indexes)
            self.motion.path_maker() # lattice_path

            if self.shared.plan.behavior_decision == "static_obstacle_avoidance":
                self.motion.weight_function_obstacle_avoidance()
                self.motion.select_trajectory()
            
            elif self.shared.plan.behavior_decision == "go_side":
                self.motion.select_trajectory()
            
            # elif self.shared.plan.behavior_decision == "stop":
            #     self.plan.trajectory.x = []
            #     self.plan.trajectory.y = []

            elif self.shared.plan.behavior_decision == "turn_right":
                self.shared.selected_lane = 2

            elif self.shared.plan.behavior_decision == "turn_left":
                self.shared.selected_lane = 0

            elif self.shared.plan.behavior_decision == "driving":
                self.motion.select_trajectory()

            sleep(self.period)