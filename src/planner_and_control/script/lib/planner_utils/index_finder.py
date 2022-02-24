from math import sqrt
from planner_and_control.msg import Ego

class IndexFinder:
    def __init__(self, ego):
        self.ego_1 = Ego()
        self.ego_1 = ego
        self.save_idx = 0
        self.current_x = self.ego_1.x
        self.current_y = self.ego_1.y
        self.index=0

    def run(self):
        min_dis=float('inf') # 무한대
        for i in range(len(self.ego_1.path.x)) :
            dx = self.current_y - self.ego_1.path.y[i]
            dy = self.current_y - self.ego_1.path.y[i]
            dis = sqrt(dx*dx + dy*dy)
            if dis < min_dis :
                min_dis=dis
                self.index = i

        print(f"ego_index : {self.index}")
   
        return self.index