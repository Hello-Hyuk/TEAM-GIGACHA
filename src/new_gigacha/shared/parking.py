from .path import Path


class Parking():
    def __init__(self):
        self.on = False
        self.mindex = 0
        self.forward_path = Path()
        self.backward_path = Path()
        self.direction = 0
        self.index = 0
        self.stop_index = 0
        self.select_num = 2