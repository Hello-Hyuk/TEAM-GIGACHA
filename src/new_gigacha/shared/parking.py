from .path import Path
from planner.sub_function.parking_function import findParkingPath
from math import hypot


class Parking():
    def __init__(self, eg, path):
        # Local to Ego
        self.ego = eg
        self.global_path = path

        self.on = False
        self.mindex = 0
        self.forward_path = Path()
        self.backward_path = Path()
        self.direction = 0
        self.index = 0
        self.stop_index = 0

    def make_parking_tra(self):
        if len(self.forward_path.x) == 0:
            self.forward_path, self.backward_path, self.mindex = findParkingPath(
                self.ego, self.global_path)

    def park_index_finder(self):
        min_dis = -1
        min_idx = 0
        step_size = 10
        save_idx = self.index

        for i in range(max(self.index - step_size, 0), self.index + step_size):
            try:
                dis = hypot(
                    self.global_path.x[i] - self.ego.x, self.global_path.y[i] - self.ego.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and save_idx <= i:
                min_dis = dis
                min_idx = i
                save_idx = i

        self.index = min_idx

    def parking_drive(self, direction):
        self.on = True
        self.direction = direction
        self.index = self.park_index_finder()
        if self.direction == 0:
            self.stop_index = len(self.forward_path.x)
        elif self.direction == 2:
            self.stop_index = len(self.backward_path.x)

        print(self.direction)
        print('park_mindex:{}'.format(self.mindex))
        print('stop_index:{}'.format(self.stop_index))
        print('parking.index:{}'.format(self.index))
