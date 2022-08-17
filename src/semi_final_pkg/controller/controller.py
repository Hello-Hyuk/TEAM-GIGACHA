import threading
from time import sleep
from .lat_controller import LatController
from .lon_controller import LonController

class Controller(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego

        self.lat_controller = LatController(self.ego, self.shared)
        self.lon_controller = LonController(self.ego, self.shared)

    def run(self):
        while True:
            try:
                self.ego.input_steer = self.lat_controller.run()
                self.ego.input_speed = self.lon_controller.run()
                # self.ego.input_brake = self.ego.target_brake
                # self.ego.input_gear = self.ego.target_gear
                
                if self.ego.input_speed == 10 and self.ego.input_steer > 7:
                    self.ego.input_speed = 5

            except IndexError:
                print("+++++++controller++++++")

            sleep(self.period)