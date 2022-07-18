import threading
from time import sleep
from lat_controller import LatController
from lon_controller import LonController

class Controller(threading.Thread):
    def __init__(self, parent, rate):
        super().__init__()
        self.period = 1.0 / rate
        self.shared = parent.shared
        self.ego = parent.shared.ego
        self.plan = parent.shared.plan

        self.lat_controller = Latcontroller(self.ego, self.shared.lattice_path, self.shared.selected_lane))
        self.lon_controller = LonController(self.ego)

    def run(self):
        while True:
            try:
                self.ego.input_steer = self.lat_controller.run()
                self.ego.input_speed, self.ego.input_brake = self.lon_controller.run()
                
                if self.ego.input_steer > 12:
                    self.ego.input_speed = 7

            except IndexError:
                print("+++++++controller++++++")
            sleep(self.period)