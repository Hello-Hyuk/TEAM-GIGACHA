import threading
from time import sleep

class BehaviorPlanner(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
    
    def run(self):
        while True:
            self.ego.speed = 1
            sleep(self.period)