#!/usr/bin/env python3
import threading
from time import sleep
from math import hypot
from localizer.gps import GPS

class MP(threading.Thread):
    def __init__(self, parent, rate):
        self.period = 1.0 / rate
        self.global_path = parent.shared.global_path
        self.shared = parent.shared

        self.ego = parent.shared.ego
        self.gps = GPS()

        self.stop_thread = False

    def map_maker(self):
        self.global_path.x.append(self.gps.x)
        self.global_path.y.append(self.gps.y)

    def run(self):
        while True:
            if not self.stop_thread:
                if round(self.pulse) % 6 == 0:
                    self.map_maker()

                if len(self.global_path.x) >= 100 and hypot(self.gps.x, self.gps.y) <= 0.96:
                    self.stop_thread = True
                    self.shared.state = "2nd"
            else:
                sleep(self.period)