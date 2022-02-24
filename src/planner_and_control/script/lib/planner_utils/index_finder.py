from math import hypot
from planner_and_control.msg import Path
from math import sqrt

class IndexFinder:
    def __init__(self, ego):
        self.ego = ego
        self.save_idx = 0
        self.current_x = self.ego.x
        self.current_y = self.ego.y
        self.ego.index=0
        

    def run(self):
        min_dis=float('inf') # 무한대
        for i in range(len(self.ego.path.x)) :
            dx = self.current_y - self.ego.path.y[i]
            dy = self.current_y - self.ego.path.y[i]
            dis = sqrt(dx*dx + dy*dy)
            if dis < min_dis :
                min_dis=dis
                self.ego.index = i

        print(f"ego_index : {self.ego.index}")
   
        return self.ego.index