import threading
from time import sleep
from math import hypot, cos, sin, degrees, atan2, radians, pi,sqrt
import numpy as np

class LonController(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego

######### curve speed control 
    def run(self): 
        while True:
            try:
                self.ego.input_speed = self.ego.target_speed
                self.ego.input_brake = self.ego.target_brake
            except IndexError:
                print("+++++++++++++++++")

            sleep(self.period)