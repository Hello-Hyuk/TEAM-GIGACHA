
from math import hypot
from planner_and_control.msg import Ego
from lib.general_utils.read_global_path import read_global_path
from planner_and_control.msg import Path

class IndexFinder:
    def __init__(self, ego):
        self.ego_1 = Ego()
        self.ego_1 = ego
        self.save_idx = 0
        self.index = 0
        self.path = read_global_path('all_nodes')

    def run(self):

        min_dis = -1
        min_idx = 0
        
        print(f"Global path length: {len(self.path.x)}")
        step_size = 100

        for i in range(max(self.index - step_size, 0), self.index + step_size):
            try:
                dis = hypot(self.path.x[i] - self.ego_1.x, self.path.y[i] - self.ego_1.y)
            except IndexError:
                break
            if (min_dis > dis or min_dis == -1) and self.save_idx <= i:
                min_dis = dis
                min_idx = i
                self.save_idx = i

        self.index = min_idx
        print(self.index)
        return self.index